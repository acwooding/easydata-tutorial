import gzip
import hashlib
import joblib
import os
import pathlib
import requests
import shutil
import tarfile
import tempfile
import zipfile
import zlib
import requests
import joblib
import gdown

from tqdm.auto import tqdm

from .. import paths
from ..log import logger

__all__ = [
    'available_hashes',
    'fetch_file',
    'fetch_files',
    'fetch_text_file',
    'get_dataset_filename',
    'hash_file',
    'hash_object',
    'infer_filename',
    'unpack',
]

_HASH_FUNCTION_MAP = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'size': os.path.getsize,
}

def safe_symlink(target, link_name, overwrite=False):
    '''
    Create a symbolic link named link_name pointing to target.
    If link_name exists then FileExistsError is raised, unless overwrite=True.
    When trying to overwrite a directory, IsADirectoryError is raised.
    '''

    if not overwrite:
        os.symlink(target, link_name)
        return

    # os.replace() may fail if files are on different filesystems
    link_dir = os.path.dirname(link_name)

    # Create link to target with temporary filename
    while True:
        temp_link_name = tempfile.mktemp(dir=link_dir)

        # os.* functions mimic as closely as possible system functions
        # The POSIX symlink() returns EEXIST if link_name already exists
        # https://pubs.opengroup.org/onlinepubs/9699919799/functions/symlink.html
        try:
            os.symlink(target, temp_link_name)
            break
        except FileExistsError:
            pass

    # Replace link_name with temp_link_name
    try:
        # Pre-empt os.replace on a directory with a nicer message
        if not os.path.islink(link_name) and os.path.isdir(link_name):
            raise IsADirectoryError(f"Cannot symlink over existing directory: '{link_name}'")
        os.replace(temp_link_name, link_name)
    except:
        if os.path.islink(temp_link_name):
            os.remove(temp_link_name)
        raise


def available_hashes():
    """Valid Hash Functions

    This function simply returns the dict known hash function
    algorithms.

    It exists to allow for a description of the mapping for
    each of the valid strings.

    The hash functions are:

    ============     ====================================
    Algorithm        Function
    ============     ====================================
    md5              hashlib.md5
    sha1             hashlib.sha1
    size             os.path.getsize
    ============     ====================================

    >>> list(available_hashes().keys())
    ['md5', 'sha1', 'size']
    """
    return _HASH_FUNCTION_MAP

def hash_object(obj, hash_type="sha1"):
    '''compute the hash of a python object

    Parameters
    ----------
    hash_type: {'md5', 'sha1', 'size'}
        hash function to use.
        Must be in `available_hashes`

    Returns
    -------
    A string: f"{hash_type}:{hash_value}"
    '''
    data_hash = joblib.hash(obj, hash_name=hash_type).hexdigest()
    return f"{hash_type}:{data_hash}"

def hash_file(fname, algorithm="sha1", block_size=4096):
    '''Compute the hash of an on-disk file

    hash_type: {'md5', 'sha1', 'size'}
        hash function to use.
        Must be in `available_hashes`
    block_size:
        size of chunks to read when hashing

    Returns
    -------
    String: f"{hash_type}:{hash_value}"
    '''
    if algorithm == 'size':
        hashval = _HASH_FUNCTION_MAP[algorithm]
        return f"{algorithm}:{hashval(fname)}"

    hashval = _HASH_FUNCTION_MAP[algorithm]()
    with open(fname, "rb") as fd:
        for chunk in iter(lambda: fd.read(block_size), b""):
            hashval.update(chunk)
    return f"{algorithm}:{hashval.hexdigest()}"

def tqdm_download(url, url_options=None, filename=None,
                  download_path=None,chunk_size=1024):
    """Download a URL via requests, displaying a tqdm status bar

    Parameters
    ----------
    url:
        URL to download
    url_options:
        Options passed to requests.request() for download
    filename:
        filename to save. If omitted, it's inferred from the URL
    download_path: path, default paths['raw_data_path']
        Inferred filename is relative to this path
    chunk_size:
        block size for writes

    Raises
    ------
    HTTPError if download fails

    Returns
    -------
    filename of written file
    """
    if url_options is None:
        url_options = {}
    if download_path is None:
        download_path = paths['raw_data_path']
    else:
        download_path = pathlib.Path(download_path)
    if filename is None:
        fn = url.split("/")[-1]
        logger.debug(f"filename not specified. Inferring '{fn}' from url")
        filename = download_path / fn
    else:
        filename = pathlib.Path(filename)
    resp = requests.get(url, stream=True, **url_options)
    total = int(resp.headers.get('content-length', 0))
    with open(filename, 'wb') as file, tqdm(
            desc=filename.name,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)
    resp.raise_for_status()

    return filename

def fetch_files(force=False, dst_dir=None, **kwargs):
    '''
    fetches a list of files via URL

    url_list: list of dicts, each containing:
        url:
            url to be downloaded
        hash_type:
            Type of hash to compute
        hash_value: (optional)
            if specified, the hash of the downloaded file will be
            checked against this value
        name: (optional)
            Name of this dataset component
        fetch_action: {'copy', 'message', 'url'}
            Method used to obtain file
        raw_file:
            output file name. If not specified, use the last
            component of the URL

    Examples
    --------
    >>> fetch_files()
    Traceback (most recent call last):
      ...
    Exception: One of `file_name`, `url`, or `source_file` is required
    '''
    url_list = kwargs.get('url_list', None)
    if not url_list:
        return fetch_file(force=force, dst_dir=dst_dir, **kwargs)
    result_list = []
    for url_dict in url_list:
        name = url_dict.get('name', None)
        if name is None:
            name = url_dict.get('url', 'dataset')
        logger.debug(f"Ready to fetch {name}")
        result_list.append(fetch_file(force=force, dst_dir=dst_dir, **url_dict))
    return all([r[0] for r in result_list]), result_list

def fetch_text_file(url, file_name=None, dst_dir=None, force=True, **kwargs):
    """Fetch a text file (via URL) and return it as a string.

    Arguments
    ---------

    file_name:
        output file name. If not specified, use the last
        component of the URL
    dst_dir:
        directory to place downloaded files
    force: boolean
        normally, the URL is only downloaded if `file_name` is
        not present on the filesystem, or if the existing file has a
        bad hash. If force is True, download is always attempted.

    In addition to these options, any of `fetch_file`'s keywords may
    also be passed

    Returns
    -------
    fetched string, or None if something went wrong with the download
    """
    retlist = fetch_file(url, file_name=file_name, dst_dir=dst_dir,
                         force=force, **kwargs)
    if retlist[0]:
        _, filename, _ = retlist
        with open(filename, 'r') as txt:
            return txt.read()
    else:
        logger.warning(f'fetch of {url} failed with status: {retlist[0]}')
        return None

def infer_filename(url=None, file_name=None, source_file=None, **kwargs):
    """Infer a filename for a file-to-be-fetched.

    Parameters
    ----------
    file_name: string
        if given, this is returned as the inferred filename (as a string, in case
        if is in pathlib.Path format)
    url: string
        if supplied (and no file_name is specified), the last component of the URL is
        returned as the inferred filename
    source_file: string
        If neither file_name nor url are specified, the last component of the source file
        is returned as the inferred filename.
    """
    if file_name is not None:
        return str(file_name)
    elif url is not None:
        file_name = url.split("/")[-1]
        logger.debug(f"`file_name` not specified. Inferring from URL: {file_name}")
    elif source_file is not None:
        file_name = str(pathlib.Path(source_file).name)
        logger.debug(f"`file_name` not specified. Inferring from `source_file`: {file_name}")
    else:
        raise Exception('One of `file_name`, `url`, or `source_file` is required')
    return file_name


def fetch_file(url=None, url_options=None, contents=None,
               file_name=None, dst_dir=None,
               force=False, source_file=None,
               hash_type=None, hash_value=None,
               fetch_action=None, message=None,
               **kwargs):
    '''Fetch the raw files needed by a DataSource.

    A DataSource is usually constructed from one or more raw files.
    This function handles the process of obtaining the raw files.

    Raw files are always specified relative to paths['raw_data_path']

    If `file_name` does not exist, this will attempt to fetch or create
    the file based on the contents of `fetch_action`:
    * message:
        Display `message` to the user and fail. Used when manual intervention
        is required, such as when a licence agreement must be completed.
    * copy:
        Copies the file from somewhere in the filesystem (`source_file`).
        WARNING: This approach rarely leads to a reproducible data workflow
    * url:
        Fetches the source file from `url`
    * create:
        File will be created from the contents of `contents`

    If `file_name` already exists, compute the hash of the on-disk file
    and check

    contents:
        contents of file to be created (if fetch_action == 'create')
    url:
        url to be downloaded
    hash_type: {'md5', 'sha1'}
        Type of hash to compute. Should not be used with hash_value, as it is already specified there.
    hash_value: String (optional)
        "{hash_type}:{hash_hexvalue}" where "hash_type" in {'md5', 'sha1'}
        and hash_hexvalue is a hex-encoded string representing the hash value.
        if specified, the hash of the downloaded file will be
        checked against this value.
    name: (optional)
        Name of this dataset component
    message: string
        Text to be displayed to user (if fetch_action == 'message')
    fetch_action: {'copy', 'message', 'url', 'create'}
        Method used to obtain file
    url_options: dict
        kwargs to pass when fetching URLs using requests
    file_name:
        output file name. If not specified, use the last
        component of the URL
    dst_dir:
        Can be used to override the default raw file location
        (paths['raw_data_path'])
    force: boolean
        normally, the URL is only downloaded if `file_name` is
        not present on the filesystem, or if the existing file has a
        bad hash. If force is True, download is always attempted.
    source_file: path
        Path to source file. (if fetch_action == 'copy')
        Will be copied to `paths['raw_data_path']`

    Returns
    -------
    one of:
        (HTTP_Code, downloaded_filename, hash) (if downloaded from URL)
        (True, filename, hash) (if already exists)
        (False, [error], None)
        (False, `message`, None) (if fetch_action == 'message')

    Examples
    --------
    >>> fetch_file()
    Traceback (most recent call last):
      ...
    Exception: One of `file_name`, `url`, or `source_file` is required
    '''
    _valid_fetch_actions = ('message', 'copy', 'url', 'create', 'google-drive')

    if url_options is None:
        url_options = {}
    # infer filename from url or src_path if needed
    if file_name is None:
        file_name = infer_filename(url=url, source_file=source_file)
        logger.debug(f"Inferred filename:{file_name} from url:{url}, source_file:{source_file}")
    if dst_dir is None:
        dst_dir = paths['raw_data_path']
    else:
        dst_dir = pathlib.Path(dst_dir)

    if not dst_dir.exists():
        os.makedirs(dst_dir)

    raw_data_file = dst_dir / file_name

    if fetch_action not in _valid_fetch_actions:
        # infer fetch action (for backwards compatibility)
        if contents is not None:
            fetch_action = 'create'
        elif message is not None:
            fetch_action = 'message'
        elif url is not None:
            fetch_action = 'url'
        elif source_file is not None:
            fetch_action = 'copy'
        logger.debug(f"No `fetch_action` specified. Inferring type: {fetch_action}")

    if hash_type is None:
        if hash_value is None:
            hash_type = 'sha1'
        else:
            hash_type, _ = hash_value.split(":")
    else: # hash_type is not None
        if hash_value:
            old_hash_type = hash_type
            hash_type, _ = hash_value.split(":")
            if hash_type != old_hash_type:
                logger.warning(f"Conflicting hash_type and hash_value. Using {hash_type}")

    # If the file is already present, check its hash.
    if raw_data_file.exists() and fetch_action != 'create':
        logger.debug(f"{file_name} already exists. Checking hash...")
        raw_file_hash = hash_file(raw_data_file, algorithm=hash_type)
        if hash_value is not None:
            if raw_file_hash == hash_value:
                if force is False:
                    logger.debug(f"{file_name} hash is valid. Skipping download.")
                    return True, raw_data_file, raw_file_hash
            else:  # raw_file_hash != hash_value
                logger.warning(f"{file_name} exists but has bad hash {raw_file_hash} != {hash_value}."
                               " Re-fetching.")
        else:  # hash_value is None
            if force is False:
                logger.debug(f"{file_name} exists, but no hash to check. "
                             f"Setting to {raw_file_hash}")
                return True, raw_data_file, raw_file_hash

    if url is None and contents is None and source_file is None and message is None:
        raise Exception(f"Cannot proceed: {file_name} not found on disk, and no fetch information "
                        "(`url`, `source_file`, `contents` or `message`) specified.")

    if fetch_action == 'url':
        if url is None:
            raise Exception(f"fetch_action = {fetch_action} but `url` unspecified")
        # Download the file
        try:
            logger.debug(f"fetching {url}")
            filename = tqdm_download(url, url_options=url_options, filename=raw_data_file)
            raw_file_hash = hash_file(filename, algorithm=hash_type)
            results = requests.get(url, **url_options)
            if hash_value is not None:
                if raw_file_hash != hash_value:
                    logger.error(f"Invalid hash on downloaded {file_name}"
                                 f" {raw_file_hash} != {hash_value}")
                    return False, f"Bad Hash: {raw_file_hash}", None
        except requests.exceptions.HTTPError as err:
            return False, err, None
    elif fetch_action == 'google-drive':
        if url is None:
            raise Exception(f"fetch_action = {fetch_action} but file ID unspecified (expected through url field)")
        # Download the file
        try:
            url_google_drive = f"https://drive.google.com/uc?id={url}"
            logger.debug(f"Fetch file ID {url} off of Google Drive (full URL {url_google_drive})")
            gdown.download(url_google_drive, str(raw_data_file), quiet=False)
        except Exception as err:
            return False, err, None
        raw_file_hash = hash_file(raw_data_file, algorithm=hash_type)
        return True, raw_data_file, raw_file_hash
    elif fetch_action == 'create':
        if contents is None:
            raise Exception(f"fetch_action == 'create' but `contents` unspecified")
        if hash_value is not None:
            logger.debug(f"Hash value ({hash_value}) ignored for fetch_action=='create'")
        with open(raw_data_file, 'w') as fw:
            fw.write(contents)
        logger.debug(f"Generating {file_name} hash...")
        raw_file_hash = hash_file(raw_data_file, algorithm=hash_type)
        return True, raw_data_file, raw_file_hash
    elif fetch_action == 'copy':
        if source_file is None:
            raise Exception("fetch_action == 'copy' but `copy` unspecified")
        logger.warning(f"Hardcoded paths for fetch_action == 'copy' may not be reproducible. Consider using fetch_action='message' instead")
        shutil.copyfile(source_file, raw_data_file)
        logger.debug(f"Checking hash of {file_name}...")
        raw_file_hash = hash_file(raw_data_file, algorithm=hash_type)
        source_file = pathlib.Path(source_file)
        logger.debug(f"Copying {source_file.name} to raw_data_path")
        return True, raw_data_file, raw_file_hash
    elif fetch_action == 'message':
        if message is None:
            raise Exception("fetch_action == 'copy' but `copy` unspecified")
        print(message)
        return False, message, None
    else:
        raise Exception("No valid fetch_action found: (fetch_action=='{fetch_action}')")

    logger.debug(f'Retrieved {raw_data_file.name} ({hash_type}:{raw_file_hash})')
    return results.status_code, raw_data_file, raw_file_hash

def unpack(filename, dst_dir=None, src_dir=None, create_dst=True, unpack_action=None):
    '''Unpack a compressed file

    filename: path
        file to unpack
    dst_dir: path (default paths['interim_data_path'])
        destination directory for the unpack
    src_dir: path (default paths['raw_data_path'])
        destination directory for the unpack
    create_dst: boolean
        create the destination directory if needed
    unpack_action: {'zip', 'tgz', 'tbz2', 'tar', 'gzip', 'compress', 'copy'} or None
        action to take in order to unpack this file. If None, it is inferred.
    '''
    if dst_dir is None:
        dst_dir = paths['interim_data_path']
    if src_dir is None:
        src_dir = paths['raw_data_path']

    if create_dst:
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

    # in case it is a Path
    filename = pathlib.Path(filename)
    path = str((src_dir / filename).resolve())

    if unpack_action is None:
        # infer unpack action
        if path.endswith('.zip'):
            unpack_action = 'zip'
        elif path.endswith('.tar.gz') or path.endswith('.tgz'):
            unpack_action = 'tgz'
        elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
            unpack_action = 'tbz2'
        elif path.endswith('.tar'):
            unpack_action = 'tar'
        elif path.endswith('.gz'):
            unpack_action = 'gz'
        elif path.endswith('.Z'):
            unpack_action = 'compress'
        else:
            logger.warning(f"Can't infer `unpack_action` from filename {filename.name}. Defaulting to 'copy'.")
            unpack_action = 'copy'

    archive = False
    verb = "Copying"
    if unpack_action == 'none':
        logger.debug(f"Skipping unpack for {filename.name}")
        return
    elif unpack_action == 'symlink':
        logger.debug(f"Linking {filename.name}...")
        safe_symlink(pathlib.Path(dst_dir) / path, path, overwrite=True)
        return
    elif unpack_action == 'copy':
        opener, mode = open, 'rb'
        outfile, outmode = path, 'wb'
    elif unpack_action == 'zip':
        archive = True
        verb = "Unzipping"
        opener, mode = zipfile.ZipFile, 'r'
    elif unpack_action == 'tgz':
        archive = True
        verb = "Untarring and ungzipping"
        opener, mode = tarfile.open, 'r:gz'
    elif unpack_action == 'tbz2':
        archive = True
        verb = "Untarring and unbzipping"
        opener, mode = tarfile.open, 'r:bz2'
    elif unpack_action == 'tar':
        archive = True
        verb = "Untarring"
        opener, mode = tarfile.open, 'r'
    elif unpack_action == 'gz':
        verb = "Ungzipping"
        opener, mode = gzip.open, 'rb'
        outfile, outmode = path[:-3], 'wb'
    elif unpack_action == 'compress':
        verb = "Uncompressing"
        logger.warning(".Z files are only supported on systems that ship with gzip. Trying...")
        os.system(f'gzip -f -d {path}')
        opener, mode = open, 'rb'
        path = path[:-2]
        outfile, outmode = path, 'wb'
    else:
        raise Exception(f"Unknown unpack_action: {unpack_action}")

    with opener(path, mode) as f_in:
        if archive:
            logger.debug(f"Extracting {filename.name}...")
            f_in.extractall(path=dst_dir)
        else:
            outfile = pathlib.Path(outfile).name
            logger.debug(f"{verb} {outfile}...")
            with open(pathlib.Path(dst_dir) / outfile, outmode) as f_out:
                shutil.copyfileobj(f_in, f_out)

def get_dataset_filename(ds_dict):
    """Figure out the downloaded filename for a dataset entry

    if a `file_name` key is present, use this,
    otherwise, use the last component of the `url`

    Returns the filename

    Examples
    --------
    >>> ds_dict = {'url': 'http://example.com/path/to/file.txt'}
    >>> get_dataset_filename(ds_dict)
    'file.txt'
    >>> ds_dict['file_name'] = 'new_filename.blob'
    >>> get_dataset_filename(ds_dict)
    'new_filename.blob'
    """

    file_name = ds_dict.get('file_name', None)
    url = ds_dict.get('url', [])
    if file_name is None:
        file_name = url.split("/")[-1]
    return file_name

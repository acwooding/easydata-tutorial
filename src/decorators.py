
# Singleton/SingletonDecorator.py
class SingletonDecorator:
    """Turns a class into a Singleton class

    When placed before a class definition, ensures that all
    insances of this class return the same data; i.e. editing one
    will change them all.
    """
    def __init__(self,klass):
        self.klass = klass
        self.instance = None
    def __call__(self,*args,**kwds):
        if self.instance == None:
            self.instance = self.klass(*args,**kwds)
        return self.instance

    # https://softwareengineering.stackexchange.com/questions/386755/sharing-docstrings-between-similar-functions
def is_documented_by(original):
  def wrapper(target):
    target.__doc__ = original.__doc__
    return target
  return wrapper

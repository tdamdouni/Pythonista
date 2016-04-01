import copy
import string
import logging

import ConfigParser


global logger

logger = logging.getLogger('gitsynchista')  

class BaseConfig(object):

    def getIntAttributes(self):
        return list()

    def getBooleanAttributes(self):
        return list()

    def dump(self):
      
      self._dump(self, type(self).__name__ + '.')
      
    def _dump(self, config, parent_prefix):
      
      global logger
            
      for (key, value) in config.__dict__.items():
        
        attr_type = type(getattr(config, key)).__name__
        name = parent_prefix + key
        #print attr_type
        if attr_type in ('int', 'bool', 'str'):
          logger.debug('%s=%s' % ( name, str(value)))
        else:
          self._dump(value, name + '.')

class ConfigHandler(object):
  
  def __init__(self, config_template):
    
    self.config_template = config_template
    
    
  def scan_section(self, sectionName, model):

    for option in self.config_file.options(sectionName):

      if not option in model.__dict__:
        raise Exception("configuration file contains invalid option '%s' in section '%s'" % (option, sectionName))

      if option in model.getBooleanAttributes():
        optionValue = string.upper(self.config_file.get(sectionName, option))
        if optionValue == '1' or optionValue == 'TRUE' or optionValue == 'YES' or optionValue == 'WAHR' or optionValue == 'JA' or optionValue == 'J':
          setattr(model, option, True)
        elif optionValue == '0' or optionValue == 'FALSE' or optionValue == 'NO' or optionValue == 'FALSCH' or optionValue == 'NEIN' or optionValue == 'N':
          setattr(model, option, False)
        else:
          raise Exception("Invalid Boolean vakue '%s' in option '%s' of section '%s'" % (self.config_file.get(sectionName, option), option, sectionName))

      elif option in model.getIntAttributes():
        try:
          intValue = int(self.config_file.get(sectionName, option))
          setattr(model, option, intValue)

        except Exception as e:
          raise Exception("Invalid numeric value '%s' in option '%s' of section '%s'" % (self.config_file.get(sectionName, option), option, sectionName))
                    
      else:
        setattr(model, option, self.config_file.get(sectionName, option))


  def read_config_file(self, filename):
    
    global logger
    
    logger.info("reading configuration file '%s' for config '%s'" % (filename, type(self.config_template).__name__))
    self.config_file = ConfigParser.ConfigParser()
    self.config_file.optionxform = str # make options case sensitive
    config = copy.deepcopy(self.config_template)

    error_message = None
      
    try:
      files_read = self.config_file.read([filename])
      if len(files_read) != 1:
        error_message = "Error while reading configuration file '%s'" % filename
            
    except Exception as e:
      error_message = "Error '%s' while reading configuration file '%s'" % ( str(e), filename )

    if error_message:
      raise Exception(error_message)


    for section_name in self.config_file.sections():

      if section_name in self.config_template.__dict__:
              
        sub_config = getattr(config, section_name)
        self.scan_section(section_name, sub_config)
        
      else:
        raise Exception("Configuration file contains invalid section '%s'" % section_name)
                        
    return config            


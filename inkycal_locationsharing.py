#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
A third-party module to show locations from Google Location Sharing.
Relies on the locationsharinglib from Costas Tyfoxylos (https://locationsharinglib.readthedocs.io/en/latest/index.html).
Adapted for use with Inkycal by Emily Boda.
Inkycal by aceisace.
"""

#############################################################################
#                           Required imports (do not remove)
#############################################################################

# Required for setting up this module
from inkycal.modules.template import inkycal_module
from inkycal.custom import *

#############################################################################
#                           Built-in library imports (change as desired)
#############################################################################

# Built-in libraries go here
from random import shuffle
import arrow

#############################################################################
#                         External library imports (always use try-except)
#############################################################################

# For external libraries, which require installing,
# use try...except ImportError to check if it has been installed
# If it is not found, print a short message on how to install this dependency

try:
  from locationsharinglib import Service
except ImportError:
  print('locationsharinglib is not installed! Please install with:')
  print('pip3 install locationsharinglib')

# RGLIBRARY
# try:
  # import reverse_geocoder as rg
# except ImportError:
  # print('reverse_geocoder is not installed! Please install with:')
  # print('pip3 install reverse_geocoder && sudo apt-get install libatlas-base-dev')
  

#############################################################################
#                         Filename + logging (do not remove)
#############################################################################

# Get the name of this file, set up logging for this filename

filename = os.path.basename(__file__).split('.py')[0]
logger = logging.getLogger(filename)

#############################################################################
#                         Class setup
#############################################################################

class Locationsharing(inkycal_module):
  """ Location Sharing Class
  This allows a user to display all their shared locations
  in Google Location Sharing
  """

  name = "Google Location Sharing - show the locations of those who have given you access via Google Location Sharing"

  requires = {
    'cookies_filepath': {
                    "label" : "In order for this module to work, you will need to follow these instructions: 1) Install a chrome extension to download your cookies (https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid/related). 2) Navigate to Google Maps, and log in (if you haven't already). 3) Use the extension to download your cookies. 4) Move the cookies file to your Pi. 5) Enter the full file path to your cookies file in the box below. For example: /home/pi/Inkycal/example.cookies"
                    },
    'google_email': {
                    "label": "Please enter the google email address that you used to access Google Location Sharing. For example: myemailaddress@gmail.com"
                    },
  }

  optional = {
    'my_name': {
                "label": "Enter the name that you would like your location to be listed as. Leave blank for the default: Me",
                "default": "Me"
                },
    'title': {
                "label": "Change the title of the module. Due to a Inkycal bug, if there are spaces in the title they will be removed. Leave blank for the default: Locations",
                "default": "Locations"
                },
    'names_preference': {
                "label": "If you would like to choose the order of the names, please list them below separated by commas. Example: Adam, Jackie, John"
                },
    'names_limit': {
                "label": "If you would like to limit the names to just the above list, choose 'yes'. Otherwise any names you haven't listed above will be added to the end of the list.",
                "options": ['yes', 'no'],
                "default": "no"
                },
    # removing this option since it is not necessary as long as the RGLIBRARY isn't being used
    #'options': {
    #            "label": "You can change the format of the address if you wish. The default is ['name', 'admin1']",
    #            "default": ["name", "admin1"]
    #            },
    'last_updated': {
                "label": "Show a last updated timestamp?",
                "options": ['yes', 'no'],
                "default": "yes"
                },
    'hours_option': {
                "label": "Use 12 or 24 hour formatted time for your last updated timestamp?",
                "options": ['12', '24'],
                "default": "12"
             },
  }
  ########################################################################

  # Initialise the class (do not remove)
  def __init__(self, config):
    """Initialize your module module"""

    # Initialise this module via the inkycal_module template (required)
    super().__init__(config)
    
    config = config['config']
    
    self.cookies_filepath = config['cookies_filepath']
    self.google_email = config['google_email']
    self.my_name = config['my_name']
    self.title = config['title']
    self.names_limit = config['names_limit']
    if config['names_preference'] and isinstance(config['names_preference'], str):
        self.names_preference = config['names_preference'].split(",")
    elif config['names_preference'] and isinstance(config['names_preference'],list):
        self.names_preference = config['names_preference']
    else:
        self.names_preference = []
    # RGLIBRARY
    #self.options = config['options']
    self.last_updated = config['last_updated']
    self.hours_option = config['hours_option']

    # give an OK message
    print(f'{filename} loaded')

#############################################################################
#                 Validation of module specific parameters   (optional)     #
#############################################################################

  def _validate(self):
    """Validate module-specific parameters"""
    # Check the type of module-specific parameters
    # This function is optional, but useful for debugging.

    # Here, we are checking if do_something (from init) is True/False
    #if not isinstance(self.age, int):
    #  print(f"age has to be a number, but given value is {self.age}")


#############################################################################
#                       Generating the image                                #
#############################################################################

  def generate_image(self):
    """Generate image for this module"""

    # Define new image size with respect to padding
    im_width = int(self.width - (2 * self.padding_left))
    im_height = int(self.height - (2 * self.padding_top))
    im_size = im_width, im_height
    logger.info('image size: {} x {} px'.format(im_width, im_height))

    # Use logger.info(), logger.debug(), logger.warning() to display
    # useful information for the developer
    logger.info('image size: {} x {} px'.format(im_width, im_height))

    # Create an image for black pixels and one for coloured pixels (required)
    im_black = Image.new('RGB', size = im_size, color = 'white')
    im_colour = Image.new('RGB', size = im_size, color = 'white')

    
    #################################################################

    #                    Your code goes here                        #
    
    # Write/Draw something on the image

    #   You can use these custom functions to help you create the image:
    # - write()               -> write text on the image
    # - get_fonts()           -> see which fonts are available
    # - get_system_tz()       -> Get the system's current timezone
    # - auto_fontsize()       -> Scale the fontsize to the provided height
    # - textwrap()            -> Split a paragraph into smaller lines
    # - internet_available()  -> Check if internet is available
    # - draw_border()         -> Draw a border around the specified area

    # If these aren't enough, take a look at python Pillow (imaging library)'s
    # documentation.
    service = Service(self.cookies_filepath, self.google_email)
    
    # Set some parameters for formatting locations feeds
    line_spacing = 1
    line_height = self.font.getsize('hg')[1] + line_spacing
    line_width = im_width
    max_lines = (im_height // (self.font.getsize('hg')[1] + line_spacing))

    # Calculate padding from top so the lines look centralised
    spacing_top = int( im_height % line_height / 2 )

    # Calculate line_positions
    line_positions = [
      (0, spacing_top + _ * line_height ) for _ in range(max_lines)]
    
    font = self.font
    
    locations_display = []
    names_display = []
    
    longest_name = 0
    print('')
    print('Found the locations of the following people:')
    
    """Get location info from everyone who has shared their location with you"""
    for p in service.get_all_people():
      """Get nickname of person found and create the name text"""
      # fun fact: in addition to returning all the people who have shared their location
      # with you, this also returns your own devices location! This is something I need
      # to verify by testing with other people's accounts. Anyway, p.full_name and p.nickname
      # are equal to your email address instead of your actual name when it returns your info.
      # To fix this I added this little thing so it would display your name instead of your email.
      if p.full_name == self.google_email:
          name = self.my_name + ":"
      else:
          name = p.nickname + ":"
      names_display.append(name)
    
      """Finds the longest name in the list so we can indent later"""
      name_size = font.getsize(name)[0]
      if name_size > longest_name:
          longest_name = name_size
          
      """Get city/state name"""
      # I used to get this from coordinates, but that library takes a while to load, so I
      # am now just parsing the address string. This may cause problems with intl addresses
      # but I haven't tested this yet. RGLIBRARY
      # search = rg.search((p.latitude, p.longitude))
      # """Use the format set in the settings file and create the location text"""
      # loc = ""
      # for option in range(len(self.options)):
          # if option == 0:
              # loc = search[0][self.options[option]]
          # else:
              # loc = loc +", "+ search[0][self.options[option]]

      # this is where I just parse the text of the address to get the city and state
      loc = p.address.split(",")[1].strip(" ")+", "+p.address.split(",")[2].split(" ")[1]
      print(name, loc)
      locations_display.append(loc)
    
    """If the person has set an ordered preference for the names in the settings file, reorder the display"""
    if self.names_preference != []:
      names_display_ordered = []
      locations_display_ordered = []

      """Goes through each preferred name and then each actual name and adds it to a new list if matched"""
      for o_name in self.names_preference:
          for n in range(len(names_display)):
              if o_name+":" == names_display[n]:
                  names_display_ordered.append(names_display[n])
                  locations_display_ordered.append(locations_display[n])

      """Then go through the old list and find any that weren't added and add them"""
      if self.names_limit == "no":
          for n in range(len(names_display)):
              if names_display[n] not in names_display_ordered:
                  names_display_ordered.append(names_display[n])
                  locations_display_ordered.append(locations_display[n]) 
        
      """Make the old list equal to the new ordered list"""
      names_display = names_display_ordered
      locations_display = locations_display_ordered
      
    """Add the title"""
    names_display.insert(0,self.title)
    locations_display.insert(0,'')
    
    """Add a 'last updated' timestamp, if requested"""
    if self.last_updated == "yes":
      if self.hours_option == '24':
          last_updated = "Last updated at "+arrow.utcnow().to(get_system_tz()).format("H:mm")
      else:
          last_updated = "Last updated at "+arrow.utcnow().to(get_system_tz()).format("h:mm a")
      
      """Truncate the lines, in case too many people share their location with you (in the case of timestamp"""
      if len(names_display) > max_lines-1:
          print('not enough space to show:', names_display[max_lines-1:len(names_display)])
          names_display = names_display[0:max_lines-1]
          locations_display = locations_display[0:max_lines-1]
          names_display.append(last_updated)
          locations_display.append('')
      else:
          names_display.append(last_updated)
          locations_display.append('')
    else:
      """Truncate the lines, in case too many people share their location with you"""
      if len(names_display) > max_lines:
          print('not enough space to show:', names_display[max_lines:len(names_display)])
          names_display = names_display[0:max_lines]
          locations_display = locations_display[0:max_lines]
    
    """Write the name text on the display in the first column"""
    for _ in range(len(names_display)):
      write(im_black, line_positions[_], (line_width, line_height),
        names_display[_], font = font, alignment= 'left')
        
    """Write the location text on the display in the second column"""
    # Column size is definited by the longest name in the first column
    indent_size = longest_name+6
    for _ in range(len(locations_display)):
      write(im_black, (line_positions[_][0] + indent_size, line_positions[_][1]), 
        (line_width-indent_size, line_height), locations_display[_], font = font, alignment = 'left')

    #################################################################

    # return the images ready for the display
    return im_black, im_colour


if __name__ == '__main__':
  print('running {0} in standalone mode'.format(filename))

################################################################################
# Last steps
# Wow, you made your own module for the inkycal project! Amazing :D
# To make sure this module can be used with inkycal, you need to register it with inkycal

# If not there already, copy your module to Inkycal/inkycal/modules
# Copy the full path of your module (e.g. right click->copy path), it should look like: /home/pi/Inkycal/inkycal/modules/mymodule.py or similar

# then open a python console and run:
# import Inkycal
# Inkycal.add_module('full/path/to/your/new/module.py')

# To remove your module, run the following in a python console:
# import Inkycal
# Inkycal.remove_module('filename.py') # Only the filename, e.g. 'mymodule.py' is required.

# How do I now import my module?
# from inkycal.modules import Class
# Where Class is the name of the class inside your module (e.g. Simple)

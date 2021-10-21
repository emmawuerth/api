from django.http import HttpRequest
from api.handlers.userprofile import UserHandler
from database.models import UserProfile, DeviceProfile
from _main_.utils.massenergize_errors import MassEnergizeAPIError, InvalidResourceError, ServerError, \
  CustomMassenergizeError, NotAuthorizedError
from _main_.utils.massenergize_response import MassenergizeResponse
from _main_.utils.context import Context
from _main_.settings import DEBUG
from sentry_sdk import capture_message
import json
import datetime
from typing import Tuple


class DeviceStore:

  def __init__(self):
    self.name = "Device Profile Store/DB"

  def get_device_info(self,  context: Context, args) -> Tuple[dict, MassEnergizeAPIError]:
    try:
      device = DeviceProfile.objects.filter(**args).first()
      if not device:
        return None, InvalidResourceError()
      return device, None

    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)
  
  def __device_attr_handler(new_device, args, context):
    ip_address = args.pop('ip_address', context.ip_address)
    device_type = args.pop('device_type', context.device_type)
    operating_system = args.pop('operating_system', context.operating_system)
    browser = args.pop('browser', context.browser)
    browser_version = args.pop('browser_version', context.browser_version)

    if ip_address:
        # TODO: Anything we want to do with a device's IP address can happen here
        new_device.ip_address = ip_address

    if device_type:
      new_device.device_type = device_type

    if operating_system:
      new_device.operating_system = operating_system

    if browser:
      new_device.browser = browser

    if browser_version:
      new_device.browser_version = browser_version
    
  def create_device(self, context: Context, args) -> Tuple[dict, MassEnergizeAPIError]:
    try:     
      new_device: DeviceProfile = DeviceProfile.objects.create(**args)

      self.__device_attr_handler(new_device, args, context)

      new_device.save()    
      return new_device, None

    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)
  
  def log_device(self, context: Context, args) -> Tuple[dict, MassEnergizeAPIError]:
    try:
      id = args.pop("id", None)
      device = DeviceProfile.objects.filter(id=id)
      if not device:
        return None, InvalidResourceError()
      
      device.update(**args)
      new_device = device.first()

      self.__device_attr_handler(new_device, args, context)

      new_device.save()
      return new_device, None

    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)
    
  def log_user(self, request: HttpRequest, context: Context, args) -> Tuple[dict, MassEnergizeAPIError]:
    try:
      device_id = args.pop("device_id", None)
      user_id = args.pop("user_id", None)
      device = DeviceProfile.objects.filter(id=device_id)
      user = UserProfile.objects.filter(id=user_id)
      # TODO: Timestamp here for now. We might pass it here from somewhere else later.
      date_time = datetime.datetime.now()
      if not device:
        return None, InvalidResourceError()
      
      device.update(**args)
      new_device: DeviceProfile = device.first()

      ip_address = args.pop('ip_address', context.ip_address)
      operating_system = args.pop('operating_system', context.operating_system)
      browser = args.pop('browser', context.browser)
      browser_version = args.pop('browser_version', context.browser_version)
      new_visit_log = args.pop('visit_log', context.browser_version)

      if user_id:
        new_device.update_user_profiles(user_id)

      if ip_address:
          # Anything we want to do with a device's IP address can happen here
          # TODO: Maybe we want to store a list of IP addresses in JSON
          new_device.ip_address = ip_address

      if operating_system:
          new_device.operating_system = operating_system

      if browser:
          new_device.browser = browser

      if browser_version:
          new_device.browser_version = browser_version
      
      if new_visit_log:
        new_device.update_visit_log(date_time)
      
      # Let user update handler handle the user side of device logging
      userhandler = UserHandler()
      # Pass timestamp to user
      request.context.args["date_time"] = date_time # TODO: this needs testing
      userhandler.update(request)
      
      new_device.save()
      return new_device, None

    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)
      
  def update_device(self, context: Context, args) -> Tuple[dict, MassEnergizeAPIError]:
    try:
      id = args.pop("id", None)
      device = DeviceProfile.objects.filter(id=id)
      if not device:
        return None, InvalidResourceError()
      
      device.update(**args)
      new_device = device.first()

      self.__device_attr_handler(new_device, args, context)

      new_device.save()
      return new_device, None

    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)
  
  def delete_device(self, context: Context, args) -> Tuple[dict, MassEnergizeAPIError]:
    try:
      id = args.pop('id', None)
      devices = DeviceProfile.objects.filter(id=id)
      devices.update(is_deleted=True)
      return devices.first(), None

    except Exception as e:
      capture_message(str(e), level="error")
      return None, CustomMassenergizeError(e)
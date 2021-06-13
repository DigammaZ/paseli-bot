class Location:
  def __init__(self, full_name, emote, role_name):
    self.full_name = full_name
    self.emote = emote
    self.role_name = role_name


PHM = Location(full_name='Puente Hills Mall',
               emote='🍚',
               role_name='PHM')
MPM = Location(full_name='Main Place Mall',
               emote='🍘',
               role_name='MPM')
LWM = Location(full_name='Lakewood Mall',
               emote='🍙',
               role_name='LWM')
MVM = Location(full_name='Moreno Valley Mall',
               emote='🎑',
               role_name='MVM')
IKE = Location(full_name='Ikebukuro, Tokyo, Japan',
               emote='🌾',
               role_name='池袋')

LOCATIONS = {PHM, MPM, LWM, MVM, IKE}

class RhythmGame:
  def __init__(self, logo_url, emote, emote_id, name, role_name):
    self.logo_url = logo_url
    self.emote = emote
    self.emote_id = emote_id
    self.name = name
    self.role_name = role_name


DANCERUSH = RhythmGame(logo_url='https://remywiki.com/images/4/43/DANCERUSH_STARDOM.png',
                       emote='<a:nugget:636335989966635009>',
                       emote_id='636335989966635009',
                       name='DanceRush Stardom',
                       role_name='Dance Rush Main')
DDR = RhythmGame(logo_url='https://remywiki.com/images/4/43/DDR_A20_PLUS_Logo-gold.png',
                 emote='<:DogOh:618548773076860928>',
                 emote_id='618548773076860928',
                 name='Dance Dance Revolution',
                 role_name='DDR Main')
GITADORA = RhythmGame(logo_url='https://p.eagate.573.jp/game/gfdm/gitadora_highvoltage/p/img/information/slid/slid_banner_00.jpg',
                      emote='<:karuta:646244486124535809>',
                      emote_id='646244486124535809',
                      name='Gitadora',
                      role_name='Gitadora Main')
GROOVE_COASTER = RhythmGame(logo_url='https://upload.wikimedia.org/wikipedia/en/a/a1/Groove_Coaster.jpg',
                            emote='<:thereisagorilla:708925040317562902>',
                            emote_id='708925040317562902',
                            name='Groove Coaster',
                            role_name='Groove Coaster Main')
IIDX = RhythmGame(logo_url='https://remywiki.com/images/c/cb/IIDX_28_BISTROVER_Logo.png',
                  emote='<:forever:493336449127546880>',
                  emote_id='493336449127546880',
                  name='Beatmania IIDX',
                  role_name='IIDX Main')
POPN = RhythmGame(logo_url='https://remywiki.com/images/f/fa/Pnm_Kaimei_riddles.png',
                  emote='<:banginbisco:472856357809291264>',
                  emote_id='472856357809291264',
                  name='Pop\'n Music',
                  role_name='Pop\'n Main')
PUMP = RhythmGame(logo_url='https://www.bmigaming.com/Games/Pictures/video-arcade-games/Pump-It-Up-20th-Anniversary-Edition-Dance-Arcade-Game-LX-XX-Model-Logo-Andamiro.jpg',
                  emote='<:suffer:537942900915306498>',
                  emote_id='537942900915306498',
                  name='Pump It Up',
                  role_name='Pump Main')
SDVX = RhythmGame(logo_url='https://remywiki.com/images/9/99/SDVX_EXCEED_GEAR.png',
                  emote='<:tama:428463105895563274>',
                  emote_id='428463105895563274',
                  name='Sound Voltex',
                  role_name='SDVX Main')
RHYTHM_GAMES = [DANCERUSH, DDR, GITADORA, GROOVE_COASTER, IIDX, POPN, PUMP, SDVX]

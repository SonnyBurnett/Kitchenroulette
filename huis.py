# Huis
# Aantal Personen
# Gang
#
class huis:
  def __init__(self, adres, aantal_personen, gang, naam, voorgerecht, hoofdgerecht, nagerecht,
               aantal_eters, lijst_eters):
    self.naam = naam
    self.adres = adres
    self.aantal_personen = aantal_personen
    self.gang = gang
    self.voorgerecht = voorgerecht
    self.nagerecht = nagerecht
    self.hoofdgerecht = hoofdgerecht
    self.aantal_eters = aantal_eters
    self.lijst_eters = lijst_eters

  def set_naam(self, naam):
      self.naam = naam

  def set_adres(self, adres):
      self.adres = adres

  def set_aantal_personen(self, aantal_personen):
      self.aantal_personen = aantal_personen

  def set_gang(self, gang):
      self.gang = gang

  def set_voorgerecht(self, adres):
      self.voorgerecht = adres

  def set_nagerecht(self, adres):
      self.nagerecht = adres

  def set_hoofdgerecht(self, adres):
      self.hoofdgerecht = adres

  def set_aantal_eters(self, aantal_eters):
      self.aantal_eters = aantal_eters

  def set_lijst_eters(self, lijst_eters):
      self.lijst_eters = lijst_eters

  def add_eter(self, eter):
      self.lijst_eters.append(eter)

  def get_naam(self):
      return self.naam

  def get_adres(self):
      return self.adres

  def get_aantal_personen(self):
      return self.aantal_personen

  def get_gang(self):
      return self.gang

  def get_voorgerecht(self):
      return self.voorgerecht

  def get_nagerecht(self):
      return self.nagerecht

  def get_hoofdgerecht(self):
      return self.hoofdgerecht

  def get_aantal_eters(self):
      return self.aantal_eters

  def get_lijst_eters(self):
      return self.lijst_eters


  def get_all(self):
      return [self.naam, self.adres, self.aantal_personen,self.gang, self.voorgerecht, self.hoofdgerecht, self.nagerecht]








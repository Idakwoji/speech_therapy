from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

# class Word(models.Model):
#     name = models.CharField(max_length=255)
#     correct_transcription = models.CharField(max_length=255)

#     class Meta:
#         db_table = 'words'

#     def __str__(self):
#         return f'{self.id}: {self.name}'

# class Sentence(models.Model):
#     name = models.CharField(max_length=255)
#     correct_transcription = models.CharField(max_length=255)

#     class Meta:
#         db_table = 'sentences'

#     def __str__(self):
#         return f'{self.id}: {self.name}'

class BaseItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class CatLev0(BaseItem):
    cat_lev0 = models.CharField(max_length=255)
    class Meta:
        db_table = "cat_lev0"
    def __str__(self):
        return f'{self.id}: {self.name}'
    
class CatLev1(BaseItem):
    cat_lev0 = models.ForeignKey(CatLev0, on_delete=models.CASCADE)
    cat_lev1 = models.CharField(max_length=255)
    class Meta:
        db_table = "cat_lev1"
    def __str__(self):
        return f'{self.id}: {self.name}'
    
class CatLev2(BaseItem):
    cat_lev1 = models.ForeignKey(CatLev1, on_delete=models.CASCADE)
    cat_lev2 = models.CharField(max_length=255)
    class Meta:
        db_table = "cat_lev2"
    def __str__(self):
        return f'{self.id}: {self.name}'

class CatLev3(BaseItem):
    cat_lev2 = models.ForeignKey(CatLev2, on_delete=models.CASCADE)
    cat_lev3 = models.CharField(max_length=255)
    class Meta:
        db_table = "cat_lev3"
    def __str__(self):
        return f'{self.id}: {self.name}'
    
from django.db import models

class BaseTable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True, blank=True)
    cat_lev0 = models.IntegerField(null=True, blank=True)
    cat_lev1 = models.IntegerField(null=True, blank=True)
    cat_lev2 = models.IntegerField(null=True, blank=True)
    cat_lev3 = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

class HumorEnGeluiden(BaseTable):
    class Meta:
        db_table = "HumorEnGeluiden"


class FysiekeGedrag(BaseTable):
    class Meta:
        db_table = "fysiekeGedrag"

class MuziekEnGeluid(BaseTable):
   class Meta:
        db_table = "muziekEnGeluid"
        
class TafelDekken(BaseTable):
    class Meta:
        db_table = "tafelDekken"

class PersoonlijkenBezittelijkVoornaamwoord(BaseTable):
    class Meta:
        db_table = 'PersoonlijkenBezittelijkVoornaamwoord'

class Gevaarlijk(BaseTable):
    class Meta:
        db_table = 'gevaarlijk'

class OmgaanMetSpullen(BaseTable):
    class Meta:
        db_table = 'omgaanMetSpullen'

class TandenVerzorgen(BaseTable):
    class Meta:
        db_table = 'tandenVerzorgen'

class VerbondenheidEnGevoelens(BaseTable):
    class Meta:
        db_table = 'VerbondenheidEnGevoelens'

class Gevoel(BaseTable):
    class Meta:
        db_table = 'gevoel'

class Ontbijten(BaseTable):
    class Meta:
        db_table = 'ontbijten'

class Tekenen(BaseTable):
    class Meta:
        db_table = "tekenen"

class AanUitkleding(BaseTable):
    class Meta:
        db_table = 'aanUitkleding'

class Groente(BaseTable):
    class Meta:
        db_table = 'groente'

class OpDeBeurt(BaseTable):
    class Meta:
        db_table = 'opDeBeurt'

class Tellen(BaseTable):
    class Meta:
        db_table = 'tellen'

class Afscheid(BaseTable):
    class Meta:
        db_table = 'afscheid'

class Groeten(BaseTable):
    class Meta:
        db_table = 'groeten'

class OpReis(BaseTable):
    class Meta:
        db_table = 'opReis'

class Tijd(BaseTable):
    class Meta:
        db_table = 'tijd'

class AlgemeenMensen(BaseTable):
    class Meta:
        db_table = 'algemeenMensen'

class Gymnastiek(BaseTable):
    class Meta:
        db_table = 'gymnastiek'

class OpenEnDichtDoen(BaseTable):
    class Meta:
        db_table = 'openEnDichtDoen'

class Toeval(BaseTable):
    class Meta:
        db_table = "toeval"

class AvondEten(BaseTable):
    class Meta:
        db_table = "avondEten"

class HaarVerzorgen(BaseTable):
    class Meta:
        db_table = "haarVerzorgen"

class Overig(BaseTable):
    class Meta:
        db_table = "overig"

class TuinEnPark(BaseTable):
    class Meta:
        db_table = "tuinEnPark"
        
class Badkamer(BaseTable):
    class Meta:
        db_table = "badkamer "

class HebbenEnDelen(BaseTable):
    class Meta:
        db_table = "hebbenEnDelen"

class Personen(BaseTable):
    class Meta:
        db_table = "personen"

class Uitjes(BaseTable):
    class Meta:
        db_table = "uitjes"
        
class Bal(BaseTable):
    class Meta:
        db_table = "bal"

class Herfst(BaseTable):
    class Meta:
        db_table = "herfst"

class Planten(BaseTable):
    class Meta:
        db_table = "planten"
        
class Vergelijken(BaseTable):
    class Meta:
        db_table = "vergelijken"
        
class BelangrijkeWoordjes(BaseTable):
    class Meta:
        db_table = "belangrijkeWoordjes"

class Huis(BaseTable):
    class Meta:
        db_table = "huis"

class PoepenEnPlassen(BaseTable):
    class Meta:
        db_table = "poepenEnPlassen"

class Verjaardag(BaseTable):
    class Meta:
        db_table = "verjaardag"

class Boerderij(BaseTable):
    class Meta:
        db_table = "boerderij"

class HuisWerken(BaseTable):
    class Meta:
        db_table = "huisWerken"

class Rekenen(BaseTable):
    class Meta:
        db_table = "rekenen"

class Voortuigen(BaseTable):
    class Meta:
        db_table = "voortuigen"

class BoodschappenDoen(BaseTable):
    class Meta:
        db_table = "boodschappenDoen"

class Huisdieren(BaseTable):
    class Meta:
        db_table = "huisdieren"

class RichtingDeWeg(BaseTable):
    class Meta:
        db_table = "richtingDeWeg"

class Vormen(BaseTable):
    class Meta:
        db_table = "vormen"

class Bos(BaseTable):
    class Meta:
        db_table = "bos"

class Kerst(BaseTable):
    class Meta:
        db_table = "kerst"

class RollenspelEnSprookjes(BaseTable):
    class Meta:
        db_table = "rollenspelEnSprookjes"
        
class Vraagwoorden(BaseTable):
    class Meta:
        db_table = "vraagwoorden"

class Buiten(BaseTable):
    class Meta:
        db_table = "buiten"

class Kleding(BaseTable):
    class Meta:
        db_table = "kleding"

class Ruimte(BaseTable):
    class Meta:
        db_table = "ruimte"

class Vuur(BaseTable):
    class Meta:
        db_table = "vuur"

class Communiceren(BaseTable):
    class Meta:
        db_table = "communiceren"

class KleineDiertjes(BaseTable):
    class Meta:
        db_table = "kleineDiertjes"

class SamenAktiviteiten(BaseTable):
    class Meta:
        db_table = "samenAktiviteiten"

class Wassen(BaseTable):
    class Meta:
        db_table = "wassen"

class Denken(BaseTable):
    class Meta:
        db_table = "denken"

class Kleuren(BaseTable):
    class Meta:
        db_table = "kleuren"

class Schoen(BaseTable):
    class Meta:
        db_table = "schoen"

class Water(BaseTable):
    class Meta:
        db_table = "water"

class Dieren(BaseTable):
    class Meta:
        db_table = "dieren"

class Knutselen(BaseTable):
    class Meta:
        db_table = "knutselen"

class Schrijven(BaseTable):
    class Meta:
        db_table = "schrijven"

class Weer(BaseTable):
    class Meta:
        db_table = "weer"

class Dierentuin(BaseTable):
    class Meta:
        db_table = "dierentuin"

class Koken(BaseTable):
    class Meta:
        db_table = "koken"

class Sinterklaas(BaseTable):
    class Meta:
        db_table = "sinterklaas"

class WegwijsInDeGroep(BaseTable):
    class Meta:
        db_table = "wegwijsInDeGroep"

class Doen(BaseTable):
    class Meta:
        db_table = "doen"

class KopjesEnBakers(BaseTable):
    class Meta:
        db_table = "kopjesEnBakers"

class Smaken(BaseTable):
    class Meta:
        db_table = "smaken"

class Welkom(BaseTable):
    class Meta:
        db_table = "welkom"

class Drankjes(BaseTable):
    class Meta:
        db_table = "drankjes"

class Kringroutines(BaseTable):
    class Meta:
        db_table = "kringroutines"

class Snoep(BaseTable):
    class Meta:
        db_table = "snoep"

class Winter(BaseTable):
    class Meta:
        db_table = "winter"

class Drinken(BaseItem):
    class Meta:
        db_table = "drinken"

class Kruipen(BaseTable):
    class Meta:
        db_table = "kruipen"

class Speelgoed(BaseTable):
    class Meta:
        db_table = "speelgoed"

class WinterKleding(BaseTable):
    class Meta:
        db_table = "winterKleding"

class Emotie(BaseTable):
    class Meta:
        db_table = "emotie"

class Lente(BaseTable):
    class Meta:
        db_table = "lente"

class Speeltuin(BaseTable):
    class Meta:
        db_table = "speeltuin"

class ZeeSwembad(BaseTable):
    class Meta:
        db_table = "zeeSwembad"

class Eruitzien(BaseTable):
    class Meta:
        db_table = "eruitzien"

class Lichaamsdelen(BaseTable):
    class Meta:
        db_table = "lichaamsdelen"

class Spelen(BaseTable):
    class Meta:
        db_table = "spelen"
        
class Ziek(BaseTable):
    class Meta:
        db_table = "ziek"
        
class Eten(BaseTable):
    class Meta:
        db_table = "eten"

class Lunch(BaseTable):
    class Meta:
        db_table = "lunch"
        
class SpelenEnWerken(BaseTable):
    class Meta:
        db_table = "spelenEnWerken"

class Zintuigen(BaseTable):
    class Meta:
        db_table = "zintuigen"

class Familie(BaseTable):
    class Meta:
        db_table = "familie"

class MensenEnRelaties(BaseTable):
    class Meta:
        db_table = "mensenEnRelaties"
        
class Spelletje(BaseTable):
    class Meta:
        db_table = "spelletje"

class Zomer(BaseTable):
    class Meta:
        db_table = "zomer"
        
class Fruit(BaseTable):
    class Meta:
        db_table = "fruit"

class Meten(BaseTable):
    class Meta:
        db_table = "meten"

class StraatEnVerkeer(BaseTable):
    class Meta:
        db_table = "straatEnVerkeer"

# standard setup of public templates database        
class PageName(models.Model):
    page_name = models.CharField(max_length=255)
    blocks = models.ManyToManyField('PageBlock', related_name='page_names', blank=True)

    def __str__(self):
        return self.page_name
    class Meta:
        # Use the exact page_name as the table name
        db_table = 'Page Names'
        using = 'public_templates'

class PageBlock(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    option = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        # Use the exact page_name as the table name
        db_table = 'Page Blocks'
        using = 'public_templates'
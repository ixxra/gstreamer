import peewee as pw
import datetime


db = pw.SqliteDatabase('models/media.db')

class BaseModel(pw.Model):
    class Meta:
        database = db


class File(BaseModel):
    uri = pw.CharField(unique=True)

    def metadata(self):
        return [tag.pair() for tag in self.tags]

    def timesPlayed(self):
        pass

    def firstPlayed(self):
        pass

    def lastPlayed(self):
        pass


class Tag(BaseModel):
    key = pw.CharField()
    value = pw.CharField()
    file = pw.ForeignKeyField(File, related_name='tags')

    def pair(self):
        return (self.key, self.value)


class LogEntry(BaseModel):
    file = pw.ForeignKeyField(File, related_name='log')
    playing_date = pw.DateTimeField(default=datetime.datetime.now)


def create_tables():
    '''
    Should be used only once
    '''
    db.connect()
    db.create_tables([File, Tag])

import discord

from trackmania.containers.records_info import RecordInfo
from trackmania.containers.track_info import TrackInfo


class TrackmaniaEmbedBuilder:
    def CreateDiscordEmbeded(self, data=[TrackInfo(), [RecordInfo(), RecordInfo()]]):
        embeded = discord.Embed()
        embeded.title = "Track name: " + data[0].TrackName
        trackAuthor = "Author: " + data[0].TrackAuthor + "\n"
        trackStyle = "Style: " + data[0].TrackStyle + "\n"
        trackLength = "TrackLength: " + data[0].TrackLength + "\n"
        embeded.description = trackAuthor + trackStyle + trackLength

        track_records = ""
        counter = 1
        for record in data[1]:
            if record.RecordType is "Dedi" and counter < 4:
                track_records += record.RecordType + " " + str(counter) + " ... " + record.Player + " [" + record.Time + "]\n"
                counter += 1

        counter = 1
        for record in data[1]:
            if record.RecordType is "Tmx" and counter < 4:
                track_records += record.RecordType + " " + str(counter) + " ... " + record.Player + " [[" + record.Time + "](" + record.ReplayUrl + ")" + "]\n"
                counter += 1

        if track_records is not "":
            embeded.add_field(name="Records:", value=track_records)
        embeded.set_image(url=data[0].TrackImageUrl)

        embeded.color = discord.Color.blue()
        return embeded

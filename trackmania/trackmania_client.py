import html
import re

import aiohttp

from trackmania.containers.records_info import RecordInfo
from trackmania.containers.track_info import TrackInfo


class TrackmaniaClient:
    # return TrackInfo() and List of RecordInfos
    async def getInfo(self, tmxID):
        url = "https://tmnforever.tm-exchange.com/main.aspx?action=trackshow&id="+tmxID+"#auto"

        # Screenshot (Not used)
        # tmxImageData = await self.getRequest(r"https://tmnforever.tm-exchange.com/main.aspx?action=trackshow&id=" + tmxID)
        # tumbnail = bool(re.search("action=trackscreenscreens&id=.*?&screentype=0", tmxImageData))

        tmxWebsiteData = await self.getRequest(url)

        trackInfo = self.getTrackInfo(tmxWebsiteData)
        trackInfo.TrackUrl = url
        trackInfo.TrackImageUrl = r"https://tmnforever.tm-exchange.com/getclean.aspx?action=trackscreenscreens&id=" + tmxID + r"&screentype=1"

        # if tumbnail:
        # trackInfo.TrackThumbnailUrl = r"https://tmnforever.tm-exchange.com/getclean.aspx?action=trackscreenscreens&id=" + tmxID + r"&screentype=0"

        recordInfos = await self.getRecordInfos(tmxWebsiteData)

        return trackInfo, recordInfos

    # returns a list of dedi records
    async def getRecordInfos(self, context):
        trackUid = re.search("id=\"ctl03_TrackUid\" value=\"(.*?)\"", context).group(1)
        dediRecordsUrl = "https://tmnforever.tm-exchange.com/get.aspx?action=apidedimania&method=onlinerecords&uid=" + trackUid

        dediRecordsData = self.getDediRecordsData(await self.getRequest(dediRecordsUrl))
        tmxRecordsData = self.getTmxRecordsData(context)
        dediRecordsData.extend(tmxRecordsData)
        return dediRecordsData

    # gets the track info from tm-exchange
    def getTrackInfo(self, context=""):
        trackInfo = TrackInfo()
        trackInfo.TrackAuthor = html.unescape(re.search(r"target=\"_blank\">(.*?)</a></TD>", context).group(1))
        trackInfo.TrackName = html.unescape(re.search(r"id=\"ctl03_ShowTrackName\">(.*?)</span>", context).group(1))
        trackInfo.TrackLength = html.unescape(re.search(r"id=\"ctl03_ShowLength\">(.*?)</span>", context).group(1))
        trackInfo.TrackStyle = html.unescape(re.search(r"id=\"ctl03_ShowStyle\">(.*?)</span>", context).group(1))
        return trackInfo

    # creates the async GET request and returns webpage data
    async def getRequest(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    # regexes information of dedimania records and returns a list
    def getDediRecordsData(self, data):
        recordsData = []
        regexData = re.findall("<td>(.*?)</td>", data)
        counter = 0
        while len(regexData) > counter:
            record = RecordInfo()
            record.RecordType = "Dedi"
            record.Player = html.unescape(regexData[counter])
            record.Server = html.unescape(regexData[counter + 1])
            record.Time = html.unescape(regexData[counter + 2])
            record.Mode = html.unescape(regexData[counter + 3])
            recordsData.append(record)
            counter += 4

        return recordsData

    def getTmxRecordsData(self, data=""):
        recordsData = []
        context = data
        while True:
            record = RecordInfo()
            record.RecordType = "Tmx"
            record.Server = "Offline"

            replay_link = re.search("get.aspx\?action=recordgbx&amp;id=(.*?)\"", context)
            if replay_link is not None:
                record.ReplayUrl = html.unescape("https://tmnforever.tm-exchange.com/get.aspx?action=recordgbx&amp;id=" + replay_link.group(1))
            else:
                break
            index = context.index("</a></td><td>")
            time = context[index - 13:index - 6]

            record.Time = time

            context = context[index + 7:]

            author = re.search("target=\"_blank\">(.*?)</a></td><td>", context).group(1)
            record.Player = html.unescape(author)
            index = context.index("</a></td><td>")
            context = context[index + 7:]

            recordsData.append(record)

        return recordsData

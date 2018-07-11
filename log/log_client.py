import discord


class LogClient:
    CanLog = False

    @staticmethod
    def Log(msg=""):
        if LogClient.CanLog is False:
            return

        print(msg)

        # You don't need loging to file. when u debug...
        # msg += "\n"
        # LogClient.LogToFile(msg)

    @staticmethod
    def LogException(message=discord.Message, exception=Exception):
        msg = "+++++++++++++++++++++++++\n"
        msg += "--------Exception--------\n"
        msg += "Discord Message: " + message.content + "\n"
        msg += "Discord Author: " + message.author.name + "\n"
        msg += "Exception Description: " + exception.__doc__ + "\n"
        msg += "Exception Class: " + exception.__class__.__name__ + "\n"
        msg += "Exception Content: " + str(exception) + "\n"
        msg += "--------Exception--------\n"
        msg += "+++++++++++++++++++++++++"

        print(msg)
        LogClient.LogToFile(msg)

    @staticmethod
    def LogToFile(msg=""):
        while True:
            try:
                with open("text_files/log.txt", "a", encoding="utf8") as file:
                    file.write(msg)
                    file.flush()
                break
            except:
                print("Failed to write to file: log.txt")
                continue

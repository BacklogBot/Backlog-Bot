from abc import ABC, abstractmethod #for abstract classes
import commandReceiver
import command

class CommandFactory(ABC):
    def __init__(self, input_bot, input_ctx):
        self.cr = commandReceiver.CommandReceiver() #create receiver 
        self.bot = input_bot
        self.ctx = input_ctx

    @abstractmethod
    def createNewCommand(self):  #factory method
        pass

class ConcreteCommandFactory(CommandFactory):
    def createNewCommand(self, command_name):  
        if command_name == "newBacklog":
            return command.NewBacklog(self.bot, self.ctx, self.cr)  #create command and associate it with receiver
        elif command_name == "helpBacklog":
            return command.HelpBacklog(self.bot, self.ctx, self.cr)  #create command and associate it with receiver
        elif command_name == "addGame":
            return command.AddGame(self.bot, self.ctx, self.cr)  #create command and associate it with receiver
        elif command_name == "delGame":
            return command.DelGame(self.bot, self.ctx, self.cr)  #create command and associate it with receiver
        elif command_name == "list":
            return command.List(self.bot, self.ctx, self.cr)  #create command and associate it with receiver
        elif command_name == "suggestGames":
            return command.SuggestGames(self.bot, self.ctx, self.cr)  #create command and associate it with receiver
        elif command_name == "editGame":
            return command.EditGame(self.bot, self.ctx, self.cr)  #create command and associate it with receiver
        elif command_name == "editBacklog":
            return command.EditBacklog(self.bot, self.ctx, self.cr)  #create command and associate it with receiver
        elif command_name == "copyGame":
            return command.CopyGame(self.bot, self.ctx, self.cr)
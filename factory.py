from abc import ABC, abstractmethod #for abstract classes
import commandReceiver
import command

class CommandFactory(ABC):
    def __init__(self, input_bot, input_ctx, input_args=None):
        '''
        arguments: 
            bot input_bot: The bot that is ordering from this factory
            context input_ctx: The context of the command entered
            str[] input_args: All the arguments provided by the user in their command call
        returns: 
            CommandFactory self: a new CommandFactory object
        modifies:
            str self.cr: The receiver object to bind to this factory
            bot self.bot: The bot that is ordering from this factory
            context self.ctx: The context of the command entered 
            str[] self.args: All the arguments provided by the user in their command call
        Description: 
            This function creates and returns and new CommandFactory object.
        '''
        self.cr = commandReceiver.CommandReceiver() #create receiver 
        self.bot = input_bot
        self.ctx = input_ctx
        self.args = input_args

    @abstractmethod
    def createNewCommand(self):  #factory method
        '''
        arguments: 
            None
        returns: 
            None
        modifies:
            None
        Description: 
            None
        '''
        pass

class ConcreteCommandFactory(CommandFactory):
    def createNewCommand(self, commandName):  
        '''
        arguments: 
            str commandName: The name of the command to be created
        returns: 
            CommandFactory self: a new Command object
        modifies:
            None
        Description: 
            This function creates and returns and new Command object.
        '''
        if commandName == "newBacklog":
            return command.NewBacklog(self.bot, self.ctx, self.cr, self.args)  #create command and associate it with receiver
        elif commandName == "helpBacklog":
            return command.HelpBacklog(self.bot, self.ctx, self.cr, self.args)  
        elif commandName == "addGame":
            return command.AddGame(self.bot, self.ctx, self.cr, self.args)
        elif commandName == "deleteGame":
            return command.DeleteGame(self.bot, self.ctx, self.cr, self.args)
        elif commandName == "list":
            return command.List(self.bot, self.ctx, self.cr, self.args)
        elif commandName == "suggestGames":
            return command.SuggestGames(self.bot, self.ctx, self.cr, self.args)
        elif commandName == "editGame":
            return command.EditGame(self.bot, self.ctx, self.cr, self.args)
        elif commandName == "editBacklog":
            return command.EditBacklog(self.bot, self.ctx, self.cr, self.args)  
        elif commandName == "copyGame":
            return command.CopyGame(self.bot, self.ctx, self.cr, self.args)
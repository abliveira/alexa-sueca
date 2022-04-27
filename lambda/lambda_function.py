# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import random

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Olá! Vamos jogar sueca! Você pode me pedir para sortiar uma cartar ou me pedir para explicar o jogo"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class PickACardIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("PickACardIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        todas_cartas = ["as", "dois", "tres", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez", "dama", "valete", "rei"]
        
        carta_tirada = random.choice(todas_cartas)
        
        # speak_output = 'Thanks, I will remember that you were born {month} {day} {year}.'.format(month=month, day=day, year=year)
        
        speak_output = 'Ok! A carta que eu tirei foi {carta_tirada}'.format(carta_tirada=carta_tirada)
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class RuleIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("RuleIntent")(handler_input)
        
    def handle(self, handler_input):

        slot = ask_utils.request_util.get_slot(handler_input, "carta")
        
        if slot.value in ["às", "ás", "as"]:
            speak_output = "Ás significa que quem tirou a carta bebe"
            
        elif slot.value in ["2", "dois", "doisinho"]:
            speak_output = "Dois significa que quem tirou a carta deve escolher duas pessoas para beberem"
            
        elif slot.value in ["3", "tres"]:
            speak_output = "Tres significa Fui à feira. Quem tirou a carta deve dizer 'Fui a feira e comprei' e então escolher \
            um item. A pessoa seguinte da roda deve repetir o que foi dito acrescentando mais um item. Quem esquecer ou trocar \
            a ordem, bebe"
        
        elif slot.value in ["4", "quatro", "quatrinho"]:
            speak_output = "Quatro significa Eu Nunca. Quem tirou a carta deve falar algo que nunca fez. Que já fez, bebe"
        
        elif slot.value in ["5", "cinco", "cinquinho"]:
            speak_output = "Cinco significa C S composto. Quem tirou a carta deve falar uma palavra que não comece com C ou S e \
            que não seja composta. A pessoa seguinte da roda deve falar uma outra palavra relacionada seguindo as mesmas regras. \
            Quem errar ou repetir uma palavra já dita, bebe"
        
        elif slot.value in ["6", "seis", "seisinho"]:
            speak_output = "Seis significa Continência. Quem tirou deve prestar Continência discretamente em qualquer momento \
            do jogo e todos os outros jogadores devem repetir o gesto. O último a prestar Continência, bebe."
        
        # elif slot.value in ["7", "sete", "setinho"]:
        #     speak_output = "Sete significa Pi Pa Pum. Quem tirou deve dizer Pi, a pessoa seguinte deve dizer Pa, e a próxima pessoa \
        #     deve dizer Pum, sempre em sentido horário. A pessoa que disser Pum deve apontar para qualquer pessoa da roda para recomeçar \
        #     a sequência novamente em sentido horário. Quem errar a sua vez ou o que deve ser dito, bebe."
            
        elif slot.value in ["7", "sete", "setinho"]:
            speak_output = "Sete significa Pi. Quem tirou deve dizer começar a contar a partir de um, e a pessoa seguinte deve continuar a contagem. \
            Sempre que o número a ser falado for múltiplo de sete ou terminar em sete, a pessoa da vez deve dizer Pi. Se errar, bebe."
            
        elif slot.value in ["8", "oito", "oitinho"]:
            speak_output = "Oito significa Pi Pa Pum. Quem tirou deve dizer Pi, a pessoa seguinte deve dizer Pa, e a próxima pessoa \
            deve dizer Pum, sempre em sentido horário. A pessoa que disser Pum deve apontar para qualquer pessoa da roda para recomeçar \
            a sequência novamente em sentido horário. Quem errar a sua vez ou o que deve ser dito, bebe."
        
        # elif slot.value in ["8", "oito", "oitinho"]:
        #     speak_output = "Oito significa Patinhos na Lagoa. Quem tirou a carta deve dizer ." 
        
        elif slot.value in ["9", "nove", "novinho", "novizinho"]:
            speak_output = "Nove significa Regra Individual. Quem tirou a carta deve escolher alguém para fazer alguma ação \
            toda vez que acontecer outra ação no jogo, incluindo beber. Se o jogador escolhido não cumprir, ele bebe."
            
        elif slot.value in ["10", "dez", "dezinho", "deizinho"]:
            speak_output = "Dez significa Regra Geral. Quem tirou deve escolher uma regra que vale para todos os jogadores. \
            Quem não cumprir a regra, bebe. Valem no máximo duas regras gerais simultaneamente."
            
        elif slot.value in ["dama", "daminha", "rainha"]:
            speak_output = "Dama significa que todas as mulheres bebem"
            
        elif slot.value in ["valete","valetinho"]:
            speak_output = "Valete significa que todos os homens bebem"
            # speak_output = '{carta_pedida} significa que todos os homens bebem'.format(carta_pedida=slot.value)
            
        elif slot.value in ["rei", "reizinho"]:
            speak_output = "Rei significa que todos bebem"
            
        else:
            speak_output = "Hmm, não sei que carta é essa"
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "O jogo é muito simples. Em sentido horário, a cada rodada um jogador me pede para \
        tirar uma carta e o jogador deve seguir a regra da carta. A qualquer momento você pode me perguntar qual o significado da carta"

        return (
            handler_input.response_builder
                .speak(speak_output)
                #.ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Ok, jogo finalizado"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, não tenho certeza. Você pode me pedir uma carta ou Ajuda. O que você gostaria de fazer?"
        reprompt = "Eu não entendi isso. Com o que posso te ajudar?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "Você acabou de acionar " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Desculpe, eu tive problemas em fazer o que você pediu. Por favor, tente novamente."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask()
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PickACardIntentHandler())
sb.add_request_handler(RuleIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

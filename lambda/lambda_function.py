# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import random
import os
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


nome_cartas = ["ás", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez", "dama", "valete", "rei"]
regra_cartas = ["Quem tirou bebe", "Duas pessoas bebem", "Pi", "Eu Nunca", "C S Composto", "Continência", "Fui à Feira e Comprei", "Vale banheiro", "Regra Individual", "Regra Geral", "Mulheres bebem", "Homens bebem", "Todos bebem"]
# regra_cartas = ["Quem tirou bebe", "Duas pessoas bebem", "Fui à Feira e Comprei", "Eu Nunca", "C S Composto", "Continência", "Pi","Pim Pa Pum", "Regra Individual", "Regra Geral", "Mulheres bebem", "Homens bebem", "Todos bebem"]

frases_carta = ["A carta que eu tirei foi", "A carta que eu sortiei foi", "A carta que eu virei foi", "Eu virei", "Eu tirei"]
frases_carta_lembrando = ["A última carta que eu tirei foi","A carta que eu tirei foi", "A carta que eu sortiei foi",  "A carta que eu virei foi", "Eu virei", "Eu tirei"]

significado_as = "Ás significa que quem tirou a carta bebe"
significado_dois = "Dois significa que quem tirou a carta deve escolher duas pessoas para beber"
significado_tres = "Três significa Pi. Quem tirou deve dizer começar a contar a partir de um, e a pessoa seguinte deve continuar a contagem. \
            Sempre que o número a ser falado for múltiplo de três ou terminar em três, a pessoa da vez deve dizer Pi. Se errar, bebe"
significado_quatro = "Quatro significa Eu Nunca. Quem tirou a carta deve falar algo que nunca fez. Quem já fez, bebe"
significado_cinco = "Cinco significa C S composto. Quem tirou a carta deve falar uma palavra que não comece com C ou S e \
            que não seja composta. A pessoa seguinte da roda deve falar uma outra palavra relacionada seguindo as mesmas regras. \
            Quem errar ou repetir uma palavra já dita, bebe"
significado_seis = "Seis significa Continência. Quem tirou deve prestar Continência discretamente em qualquer momento \
            do jogo e todos os outros jogadores devem repetir o gesto. O último a prestar Continência, bebe"
significado_sete = "Sete significa Fui à feira. É um jogo da memória, e quem tirou a carta deve dizer 'Fui a feira e comprei'\
         e então escolher um item. A pessoa seguinte da roda deve repetir o que foi dito acrescentando mais um item. Quem \
         esquecer ou trocar a ordem, bebe"
significado_oito = "Oito significa Vale banheiro. Quem tirou ganha o direito de ir no banheiro. Quem não tiver o direito e não \
        aguentar, pode ir, mas bebe duas vezes"
# significado_oito = "Oito significa Pim Pa Pum. Quem tirou deve dizer Pim, a pessoa seguinte deve dizer Pa, e a próxima pessoa \
#            deve dizer Pum, sempre em sentido horário. A pessoa que disser Pum deve apontar para qualquer pessoa da roda para recomeçar \
#            a sequência em sentido horário. Quem errar a sua vez ou o que deve ser dito, bebe"
significado_nove = "Nove significa Regra Individual. Quem tirou a carta deve escolher alguém para fazer alguma ação \
            toda vez que acontecer outra ação no jogo, incluindo beber. Se o jogador escolhido não cumprir, ele bebe"
significado_dez = "Dez significa Regra Geral. Quem tirou deve escolher uma regra que vale para todos os jogadores. \
            Por exemplo, só pode falar com sotaque. Ou é proibido dizer a palavra não. \
            Quem não cumprir a regra, bebe. Valem no máximo duas regras gerais simultaneamente"
significado_dama = "Dama significa que todas as mulheres bebem"
significado_valete = "Valete significa que todos os homens bebem"
significado_rei = "Rei significa que todos bebem"
# "Oito significa Patinhos na Lagoa. Quem tirou a carta deve dizer ." 


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Vamos jogar sueca! Você pode me pedir para sortiar uma carta ou me pedir para explicar o jogo"

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
        
        confirmacoes = ["Ok", "Ok", "Está bem", "Claro"]
        
        confirmacao = confirmacoes[random.randint(0, len(confirmacoes) - 1)] # Mede o tamanho da lista e subtrai um para usar como índice
        
        frase_tirada = frases_carta[random.randint(0, len(frases_carta) - 1)]
        
        carta_indice = random.randint(1, 13) - 1
        
        carta_tirada = nome_cartas[carta_indice]

        regra_tirada = regra_cartas[carta_indice]

        attributes_manager = handler_input.attributes_manager

        carta_attributes = {
            "last_rule": carta_indice
        }

        attributes_manager.persistent_attributes = carta_attributes
        attributes_manager.save_persistent_attributes()
        
        speak_output = '{confirmacao}! {frase_tirada} {carta_tirada}. {regra_tirada}.'.format(frase_tirada=frase_tirada, confirmacao=confirmacao, carta_tirada=carta_tirada, regra_tirada=regra_tirada)
        
        
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
        
        if slot.value in ["às", "ás", "as", "asinho"]:
            speak_output = significado_as
            
        elif slot.value in ["2", "dois", "doisinho"]:
            speak_output = significado_dois
            
        elif slot.value in ["3", "tres"]:
            speak_output = significado_tres
        
        elif slot.value in ["4", "quatro", "quatrinho"]:
            speak_output = significado_quatro
        
        elif slot.value in ["5", "cinco", "cinquinho"]:
            speak_output = significado_cinco
        
        elif slot.value in ["6", "seis", "seisinho"]:
            speak_output = significado_seis
        
        elif slot.value in ["7", "sete", "setinho"]:
            speak_output = significado_sete
            
        elif slot.value in ["8", "oito", "oitinho"]:
            speak_output = significado_oito
        
        elif slot.value in ["9", "nove", "novinho", "novizinho"]:
            speak_output = significado_nove
            
        elif slot.value in ["10", "dez", "dezinho", "deizinho"]:
            speak_output = significado_dez
            
        elif slot.value in ["dama", "daminha", "rainha"]:
            speak_output = significado_dama
            
        elif slot.value in ["valete","valetinho"]:
            speak_output = significado_valete
            
        elif slot.value in ["rei", "reizinho"]:
            speak_output = significado_rei
            
        else:
            speak_output = "Hmm, não sei que carta é essa"
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
        

class RememberCardIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = ("last_rule" in attr)

        return attributes_are_present and ask_utils.is_intent_name("RememberCardIntent")(handler_input)
        
    def handle(self, handler_input):

        attr = handler_input.attributes_manager.persistent_attributes
        last_rule = attr['last_rule']
        
        frase_tirada = frases_carta_lembrando[random.randint(0, len(frases_carta_lembrando) - 1)]     
        
        carta_tirada = nome_cartas[last_rule]

        regra_tirada = regra_cartas[last_rule]
        
        speak_output = '{frase_tirada} {carta_tirada}. {regra_tirada}.'.format(frase_tirada=frase_tirada,carta_tirada=carta_tirada, regra_tirada=regra_tirada)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class LastRuleIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = ("last_rule" in attr)

        return attributes_are_present and ask_utils.is_intent_name("LastRuleIntent")(handler_input)
        
    def handle(self, handler_input):

        attr = handler_input.attributes_manager.persistent_attributes
        last_rule = attr['last_rule']
        
        frase_tirada = frases_carta_lembrando[random.randint(0, len(frases_carta_lembrando) - 1)]
        
        carta_tirada = nome_cartas[last_rule]

        if last_rule == 0:
            regra_lembrada = significado_as
            
        elif last_rule == 1:
            regra_lembrada = significado_dois
            
        elif last_rule == 2:
            regra_lembrada = significado_tres
        
        elif last_rule == 3:
            regra_lembrada = significado_quatro
        
        elif last_rule == 4:
            regra_lembrada = significado_cinco
        
        elif last_rule == 5:
            regra_lembrada = significado_seis
        
        elif last_rule == 6:
            regra_lembrada = significado_sete
            
        elif last_rule == 7:
            regra_lembrada = significado_oito
        
        elif last_rule == 8:
            regra_lembrada = significado_nove
            
        elif last_rule == 9:
            regra_lembrada = significado_dez
            
        elif last_rule == 10:
            regra_lembrada = significado_dama
            
        elif last_rule == 11:
            regra_lembrada = significado_valete
            
        elif last_rule == 12:
            regra_lembrada = significado_rei
        
        speak_output = '{frase_tirada} {carta_tirada}. {regra_lembrada}.'.format(frase_tirada=frase_tirada,carta_tirada=carta_tirada, regra_lembrada=regra_lembrada)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class InfoIntentHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("InfoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "O jogo Sueca para Alexa foi desenvolvido por abliveira"

        return (
            handler_input.response_builder
                .speak(speak_output)
                #.ask(speak_output)
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
        tirar uma carta e o jogador deve seguir a regra da carta. A qualquer momento você pode me perguntar \
        qual o significado de uma carta ou qual foi a última carta tirada. O que você deseja?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
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
        speech = "Hmm, não tenho certeza. Você pode me pedir uma carta ou ajuda. O que você gostaria de fazer?"
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


sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PickACardIntentHandler())
sb.add_request_handler(RuleIntentHandler())
sb.add_request_handler(RememberCardIntentHandler())
sb.add_request_handler(LastRuleIntentHandler())
sb.add_request_handler(InfoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
from __future__ import print_function
from gensim.parsing.preprocessing import preprocess_string
from keras.models import load_model
try:
   	input = raw_input
except NameError:
   	pass

model = load_model('SentimentAnalysis/model_nn.h5')
def predict(tweet):
	return 1

finisher = 'finisher'

def friends():
	response = input('How are your friends meeting up with your expectations?\n')
	if(predict(response) >=0.4):
		response = input('Have you broken up with someone recently?\n')
		if(predict(response)>=0.4):
			print(name + ", don't feel sad. Take your time and heal properly, look at what's happened, learn from it, and find ways to build a new and healthy life.\nAll any of us wants is to be happy. For some, this requires the perfect person to be our other half, and for others, it means completing the equation yourself. Either way, to find the right person, you need to be the right person. And trust that in the long run, your efforts will lead to your own personal happy ending.")
			print(finisher)
		else:
			print(name + ", don't worry. You may be at a point where similar people are not in your life right now. That happens in life from time to time.\nIt is better to be away from incompatible people, and those people are attracted to you when you pretend to be someone you aren't.\nBe as different as you trully are, get to know yourself at a deep level,esteem your individulaity, interact with pepole honestly, and eventually the people who appreciate you will notice and be drawn in.")
			print(finisher)
	else:
		print("Many people tend to expect too much of others, their family, their friends or even just acquaintances. It's a usual mistake, people don't think exactly the way you do.\nDon't let the opinions of others make you forget what you deserve. You are not in this world to live up to the expectations of others, nor should you feel that others are here to live up to yours.\nThe first step you should take if you want to learn how to stop expecting too much from people is to simply realize and accept the fact that nobody is perfect and that everyone makes mistakes every now and then.")
		print(finisher)
		
def family():
    print('A4')
    print(finisher)


def work():
   print(name+", don't take too much stress.I can list some really cool ways to handle it. You should develop healthy responses which include doing regular exercise and taking good quality sleep.\nYou should have clear boundaries between your work life and home life so you make sure that you don't mix them and tecniques such as meditation, deep breathing exercises and mindfulness can be really helping in relieving stress.\n  Always take time to recharge so as to avoid the negative effects of chronic stress and burnout, we need time to replenish and return to our pre-stress level of functioning.\n This recovery process requires switching off from work by having periods of time when you are neither engaging in work-related activities, nor thinking about work. That's why it's critical that you disconnect from time to time, in a way that fits your needs and preferences.")
   print(finisher)
		

def sad4():
	print("My sympathies. Looks like it might be a point of concern. Don't worry, that's what I'm here for!")
	response_friends = input('How are things going on with your friends?\n')
	response_family  = input('How is your relationship with your parents?\n')
	response_worklife = input('How is your work or academic life going on?\n')
	if(predict(response_friends)<=0.3):
		friends()
	else:
		if(predict(response_family)<=0.3):
			family()
		else:
			work()
def sad2():
	response = input('Please feel free to share your feelings ' + name + ', think of me as your friend.\n')
	if(predict(response)>=0.3):
		response = input('I see. Among the thoughts occuring in your mind, which one upsets you the most?\n')
		response = input('Why do you think it upsets you?\n')
	        print("Okay. You just identified what we call an automatic thought. Everyone has them. They are thoughts that immediately pop to mind without any effort on your part.\nMost of the time the thought occurs so quickly you don't notice it but it has an impact on your emotions. It's usually the emotion that you notice, rather than the thought.\nOften these automatic thoughts are distorted in some way but we usually don't stop to question the validity of the thought. But today, that's what we are going to do.")
		response = input('So, ' + name + ', are there signs that contrary could be true?\n')
		if(predict(response)>=0.4):
			print("I'm glad that you realised that the opposite could be true. The reason these are called 'false beliefs' is because they are extreme ways of perceiving the world. They are black or white and ignore the shades of grey in between.\nNow that you have learned about this cool technique, you can apply it on most of the problems that you will face. If you still feel stuck at any point, you can always chat with me.\nBest of luck for your future endeavours. Bye!")
		else:
			sad4()

        else:
            sad4()
           
def sad1():
	response = input('I understand. Seems like something\'s bothering you. Could you describe it in short?\n')
	if(predict(response)>=0.4):
		response = input('Do you really need help?\n') ##
		if(predict(response)>=0.45):
			print("That's okay. It was nice talking to you. You can chat with me anytime you want.\n Bye" + name + "!")
		else:
			sad3()
	else:
		sad2()

def sad3():
	response = input('Feel comfortable. Could you briefly explain about your day?\n')
	response = input('What are the activities that make up your most of the day?\n')
	response = input('It looks like you are comfortable talking about yourself. Could you share your feelings?\n')
	if(predict(response)>=0.3):
		sad2()
	else:
		sad4()
	
print('Hello! Thanks for coming here. I am a chatbot. People say that I am a kind and approachable bot.')
name = input('Please tell me your name.\n')
name = [word for word in preprocess_string(name) if word not in ('name', 'peopl', 'call', 'friend')][0]
name = name[0].upper() + name[1:]
print("Hi " + name + "! My name's Brad. Let's start with our session.")
response = input("How are you doing?\n")
if (predict(response) >=0.5):
	response = input('That is good. Are you usually this happy?\n') ##
	if (predict(response)>=0.7):
		response = input('You seem to be really content. Wanna sign off?\n')
		if(predict(response)>=0.8):
			print('Ok, bye ' + name + '!')
		else:
			response = input('Is there something bothering you?') ##
			if(predict(response)>=0.9):
				print("That's okay. It was nice talking to you. You can chat with me anytime you want.\n Bye" + name + "!")
			else:
				sad1()
	else:
		sad1()
else:
	sad3()

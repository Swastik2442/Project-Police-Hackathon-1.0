from .models import Feedback

experienceEN = {1: 'Very Bad', 2: 'Bad', 3: 'Neutral', 4: 'Good', 5: 'Very Good'}
experienceHI = {1: 'बहुत बुरा', 2: 'बुरा', 3: 'निष्पक्ष', 4: 'अच्छा', 5: 'बहुत अच्छा'}

def getMessageFromFeedback(feedback: Feedback, language='en'):
    """Returns the Message that can be sent from a submitted Feedback."""
    message = ""
    user = feedback.submittedBy
    userName = user.first_name + ' ' + user.last_name
    if language == 'en':
        message = f"""Dear {userName},
Thank You for submitting the Feedback for the {feedback.forStation.name}.
You had a {experienceEN[int(feedback.experience)]} experience at the station. We hope that you will have a better experience next time.
Rajasthan Police"""
    elif language == 'hi':
        message = f"""प्रिय {userName},
{feedback.forStation.name} के लिए फीडबैक जमा करने के लिए धन्यवाद।
पुलिस स्टेशन में आपका अनुभव {experienceHI[int(feedback.experience)]} रहा। हमें उम्मीद है कि अगली बार आपको अनुभव बेहतर होगा।
राजस्थान पुलिस"""
    return message
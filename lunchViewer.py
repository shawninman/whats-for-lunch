import json
import arrow
import random
import requests

def lambda_handler(event, context):    
    host = 'https://api.mealviewer.com/api/v4/school'
    school = 'HeritageES'
    tomorrow = arrow.utcnow().to('US/Eastern').shift(days=1)

    if tomorrow.weekday() in (5, 6):
        output = "There's no school tomorrow, silly! Are you pulling my leg?"
    else:
        formatted_tomorrow = tomorrow.format('MM-DD-YYYY')

        url = f'{host}/{school}/{formatted_tomorrow}/{formatted_tomorrow}/0'
        r = requests.get(url)
        menus = r.json().get('menuSchedules')[0].get('menuBlocks')
        
        if not menus:
            output = "Quack, quack. There's no school tomorrow, you lucky ducks!"
        else:
            lunch_menu = menus[1]
        
            entrees = [food['item_Name'].strip() for food in lunch_menu.get('cafeteriaLineList').get('data')[0]['foodItemList']['data'] if food['item_Type'] == 'Entrees']

            entree_descriptor = '{0}, and {1}'.format(', '.join(entrees[:-1]), entrees[-1])

            if 'taco' in entree_descriptor.lower():
                output = f"It's your lucky day, amigos! Take your pick from {entree_descriptor}."
            elif 'brunch' in entree_descriptor.lower():
                output = f"Bring a steaming cup of hot cocoa and bath robe kiddos, it's brunch for lunch! Choose from {entree_descriptor}."
            elif 'turkey' in entree_descriptor.lower():
                output = f"Gobble, gobble. Get ready for {entree_descriptor}."
            else:
                adjective = random.choice(['delicious', 'scrumptious', 'amazing', 'delightful', 'spectacular', 'wonderful', 'stupendous', 'unbelievable'])
                output = f"Tomorrow's {adjective} entrees include {entree_descriptor}!"
            
    return {
        'statusCode': 200,
        'body': json.dumps(output)
    }

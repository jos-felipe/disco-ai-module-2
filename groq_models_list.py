# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    groq_models_list.py                                :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: josfelip <josfelip@student.42sp.org.br>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/02/26 14:37:13 by josfelip          #+#    #+#              #
#    Updated: 2025/02/26 14:37:14 by josfelip         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
from groq import Groq
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# List models
try:
    models = client.models.list()
    print("Available Models on Groq:")
    for model in models.data:
        print(f"- {model.id}")
except Exception as e:
    print(f"Error listing models: {e}")
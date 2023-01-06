import argparse
import os
import openai
from subprocess import call
import sys

# Set up the OpenAI API client
openai.api_key = os.getenv('GPT_API_KEY')

# Set up the model and prompt
model_engine = "text-davinci-003"

# List of negative answers
ways_to_say_no = ["no", "n"]
ways_to_say_yes = ["yes", "y"]

def user_said(user_response, allowed_responses):
		for allowed_response in allowed_responses:
						if user_response.lower() == allowed_response:
								return True
		return False

def generate(prompt_in):
		completion = openai.Completion.create(
				engine=model_engine,
				prompt=prompt_in,
				max_tokens=1024,
				n=1,
				stop=None,
				temperature=0.5,
		)

		return (completion.choices[0].text)[2:]

if __name__ == '__main__':
		parser = argparse.ArgumentParser()
		parser.add_argument('-p', '--prompt', required=True, type=str, help='Content of the prompt')
		parser.add_argument('-f', '--file-name', required=True, type=str, help='Name of the C++ source file')
		parser.add_argument('-sp', '--source-path', required=True, type=str, help='Path for the generated C++ source files')
		args, unknown = parser.parse_known_args()

		#
		# Generate the code and ask feedback from the user
		#
		cpp_prompt = args.prompt

		while True:
				print("\nGenerating code ... ")
				cpp_source_code = generate(cpp_prompt)
				print("Done.\n\nGPT generated code:\n" + cpp_source_code + "\n")

				# Get user's response and check if the answer makes sense by counting the charecters in the response
				answer = ""
				while True:
						answer = input("Needs refinement? (describe the refinements or type 'no'): ")

						if len(answer) < 10 and not user_said(answer, ways_to_say_no):
								print ("\nNot sure if I understood you. ")
								continue
						else:
								break

				# Check if the user said no or wants to refine the code
				if user_said(answer, ways_to_say_no):
						break

				cpp_prompt = "I will provide you a C++ source code. Please modify it according to this description: '"\
						+ answer \
						+ "'. Here is the C++ code: '" \
						+ cpp_source_code + "'."

		# Write the C++ code to a file
		full_path = args.source_path + args.file_name

		with open(full_path, "w") as f:
				f.write(cpp_source_code)
				print ("C++ source file created in: '" + full_path + "'.")

		#
		# Generate the compilation command
		#
		answer = ""
		while True:
				answer = input("Compile the code? (yes/no): ")

				if len(answer) < 1 and len(answer) > 3 \
						or not user_said(answer, ways_to_say_yes) \
						and not user_said(answer, ways_to_say_no) :

						print ("\nNot sure if I understood you. ")
						continue
				else:
						break

		if user_said(answer, ways_to_say_no):
				sys.exit("Code not compiled. Exiting.")

		gpp_prompt = "I will provide you a C++ source code and I want you to create the g++ command that compiles the code. Use '" \
				+ args.file_name \
				+ "' as the name of the source file in the g++ command." \
				+ "'. Here is the C++ code: '" \
				+ cpp_source_code + "'."

		gpp_command_raw = generate(gpp_prompt)

		# Clean up the g++ command
		gpp_token_found = False
		gpp_command_tokens = gpp_command_raw.split()

		for command_token in gpp_command_tokens:
				if command_token == "g++":
						gpp_token_found = True
						break

		if not gpp_token_found:
				print ("GPT generated the following command: '" + gpp_command_raw + "'")
				sys.exit("This is not a valid g++ command, exiting.")

		# Remove all tokens before the g++ token. Note that there might be multiple g++ token
		while gpp_command_tokens.count('g++') > 1:
				index = gpp_command_tokens.index('g++')
				gpp_command_tokens = gpp_command_tokens[index + 1:]

		index = gpp_command_tokens.index('g++')
		gpp_command_tokens = gpp_command_tokens[index:]

		# Concatenate the tokens just to print the command to the user
		gpp_command_str = gpp_command_tokens[0]
		for token in gpp_command_tokens[1:]:
				gpp_command_str = gpp_command_str + " " + token

		print ("\nCompiling the generated C++ code via: '" + gpp_command_str + "' ... \n")
		cwd = os.getcwd()
		os.chdir(args.source_path)
		call(gpp_command_tokens)
		os.chdir(cwd)
		print ("Done.\n")

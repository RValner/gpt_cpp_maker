import argparse
import os
import openai
from subprocess import call
import sys

if __name__ == '__main__':
		parser = argparse.ArgumentParser()
		parser.add_argument('-p', '--prompt', required=True, type=str, help='Content of the prompt')
		parser.add_argument('-f', '--file-name', required=True, type=str, help='Name of the C++ source file')
		parser.add_argument('-sp', '--source-path', required=True, type=str, help='Path for the generated C++ source files')
		args, unknown = parser.parse_known_args()

		# Set up the OpenAI API client
		openai.api_key = os.getenv('GPT_API_KEY')

		# Set up the model and prompt
		model_engine = "text-davinci-003"

		# Generate the source code
		cpp_prompt = args.prompt

		completion = openai.Completion.create(
				engine=model_engine,
				prompt=cpp_prompt,
				max_tokens=1024,
				n=1,
				stop=None,
				temperature=0.5,
		)

		cpp_source_code = (completion.choices[0].text)[2:]

		# Generate the compilation command
		gpp_prompt = "Create the g++ compilation command that compiles this program. Use '" + args.file_name + "' as the name of the source file."

		completion = openai.Completion.create(
				engine=model_engine,
				prompt=gpp_prompt,
				max_tokens=1024,
				n=1,
				stop=None,
				temperature=0.5,
		)

		gpp_command = (completion.choices[0].text)[2:]

		# Write the C++ code to a file
		full_path = args.source_path + args.file_name

		with open(full_path, "w") as f:
				f.write(cpp_source_code)

		print("========================")
		print(" C++ source code:")
		print("========================\n")
		print(cpp_source_code + '\n')

		print("========================")
		print(" g++ compiler command:")
		print("========================\n")
		print(gpp_command)

		# Compile the program
		gpp_command_tokens = gpp_command.split()

		if gpp_command_tokens[0] != "g++":
			sys.exit("This is not a g++ command, exiting.")

		cwd = os.getcwd()
		os.chdir(args.source_path)
		call(gpp_command_tokens)
		os.chdir(cwd)

		print ("C++ program created.")

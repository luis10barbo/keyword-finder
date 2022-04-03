from fileinput import filename
import json
import logging
import os
import traceback


def main():
    # Input to get keywords
    # Save keywords
    # Use keywords to recursively search all files in path
    
    logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w")
    
    def error(message:str=""):
        print(f"ERROR >> {message}")
        logging.error(message)

    def info(message:str=""):
        print(f"INFO >> {message}")
        logging.info(message)
    
    def prompt(question:str="", predefined_answer:str="") -> str:
        answer = ""
        
        while answer == "":
            answer = input(f"{question}? (y/n): ")
            clear()
            
            if answer != "y" and answer != "n":
                print("Please type a valid answer.")
                answer = ""

        return answer
    
    def clear() -> None:
        os.system("clear")
    
    class Search:
        def __init__(self) -> None: 
            self.config:dict = {
                "keywords": [],
                "path": "",
            }
            self.matches:dict[str, set] = {}
            self.config_file_path:str = f"{os.path.join(os.getcwd(), 'config.json')}"

            self.open_config()
            
            if self.config == {"keywords": [],"path": "",}:   
                self.prompt_keywords()
                self.prompt_path()
                
            self.save_config()
            
            self.search_files(self.config["path"])
            
           
            
        def save_config(self) -> None:
            with open(self.config_file_path, "w", encoding="utf-8") as file:
                json.dump(self.config, file, indent=4)
            return 0
                
        def open_config(self) -> None:
            answer = prompt("Do you wish to use saved config")
            if answer == "n":
                return 0
            
            if os.path.isfile(self.config_file_path) == False:
                return 1
            
            with open(self.config_file_path, "r", encoding="utf-8") as file:
                self.config = json.load(file)
                return 0
        
        def prompt_keywords(self) -> None:
            answer = ""
            while answer.replace(" ", "") == "":
                answer = input("Type the keywords that you want to search for separated by spaces: ")
                clear()

                if answer == "":
                    print("Please type a valid answer.")
            
            self.config["keywords"] = answer.split(" ")

        def prompt_path(self) -> None:
            answer = ""
            path = ""

            while answer == "":
                answer = input("Type the directory that you want to search: ")

                if os.path.isdir(answer) == False:
                    print("Please type a valid directory.")
                    answer = ""
                else:
                    path = answer
                    answer = prompt(f"Do you really want to search {answer}")
                    answer = "" if answer == "n" else answer
                    
            self.config["path"] = path
            
            return 0
        
        def match_for_keywords(self, file_path:str) -> None:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    file_text = file.read()
                
                # Loop through keywords
                for keyword in self.config["keywords"]:
                    if keyword in file_text:
                        info(f"Keyword '{keyword}' found at file '{file_path}'")
                        if f"{file_path}" not in self.matches:
                            self.matches[f"{file_path}"] = set()
                        
                        # Add keyword to set in dict with path as keyword
                        self.matches[f"{file_path}"].add(keyword)
                        
            except Exception:
                logging.exception("")
                error(f"An error has occoured while trying to match for keywords at file {file_path}")
                return 1
            
            info(f"End of file'{file_path}'")
            return 0

            
        def search_files(self, path="") -> None:
            files = os.listdir(path)
            
            # Loop through files
            for file in files:
                # Current file path
                file_path = os.path.join(path, file)
                
                # If file is directory, open it and search children files
                if os.path.isdir(file_path):
                    info(f"Opening folder '{file_path}'")
                    self.search_files(path=file_path)
                # Else open and match for keywords
                else:
                    info(f"Opening file '{file_path}'")
                    self.match_for_keywords(file_path=file_path)
            
            info(f"End of folder'{path}'")
            return 0
                
            
                        
    search = Search()       
    print(search.matches)
    
    pass

if __name__ == "__main__":
    main()
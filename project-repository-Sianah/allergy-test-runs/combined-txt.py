file_names = [
    'allergy-detection-gpt/allergy documents-txt/Dust_Mite_Allergy_Summary.txt',
    'allergy-detection-gpt/allergy documents-txt/Egg_Allergy_Summary.txt',
    'allergy-detection-gpt/allergy documents-txt/Food_Allergy_Summary.txt',
    'allergy-detection-gpt/allergy documents-txt/Fish_Allergy_Summary.txt',
    'allergy-detection-gpt/allergy documents-txt/Hay_Fever_Summary.txt',
    'allergy-detection-gpt/allergy documents-txt/Milk_and_Dairy_Allergy_Summary.txt',
    'allergy-detection-gpt/allergy documents-txt/Peanut_Allergy_Summary.txt',
    'allergy-detection-gpt/allergy documents-txt/Pet_Allergy_Summary.txt',
    'allergy-detection-gpt/allergy documents-txt/Shellfish_Allergy_Summary.txt',
    'allergy-detection-gpt/allergy documents-txt/Soy_Allergy_Summary.txt',
    'allergy-detection-gpt/allergy documents-txt/Tree_Nut_Allergy_Summary.txt',
    'allergy-detection-gpt/allergy documents-txt/Wheat_and_Gluten_Summary.txt',
    # Add the full path for any additional files here
]

output_file_path = 'allergy-detection-gpt/allergy documents-txt/allergy_summaries_combined.txt'

with open(output_file_path, 'w') as outfile:
    for fname in file_names:
        with open(fname) as infile:
            outfile.write(infile.read() + "\n\n")


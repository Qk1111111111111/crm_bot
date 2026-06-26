prompt_screen_body = ''' 
Извлеки из изображения только указанные поля.

Верни строго JSON без пояснений, без текста, без markdown.

Если значение отсутствует — используй null.

Поля:
{'measurement_date': <дата и время измерения>,
'weight_kg': <вес в кг>,
'skeletal_muscle_mass_kg': <масса скелетных мышц в кг>,
'body_fat_mass_kg': <масса жира в кг>,
'bmi_kg_per_m2': <ИМТ в кг/м2>,
'body_fat_percentage': <процент жира в теле>}
'''
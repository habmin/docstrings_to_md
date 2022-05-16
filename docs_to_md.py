import inspect
import re
import sys
import pathlib
sys.path.append(f"{pathlib.Path(__file__).parent.absolute()}/Graphical-App")

# ------------------------------------------------------

def format_body(list_string):
    new_body = "";
    for line in list_string:
        if ":" in line or line == "None":
            new_body += f"__{line.lstrip()}__\n\n"
        elif not line:
            pass
        elif "__" in line:
            new_body += f"{line}\n\n"
        else:
            new_body += f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{line.lstrip()}\n\n"
    return new_body

def format_function_body(get_doc):
    if not type(get_doc) == str:
        return
    new_body = ""
    body_group = ""
    if "Raises" in get_doc:
        body_group = re.compile(r"(.*)(Parameters\s*----------\s*)(.*)(Raises\s*------\s*)(.*)(Returns\s*-------\s*)(.*)", re.M | re.S)
    else:
        body_group = re.compile(r"(.*)(Parameters\s*----------\s*)(.*)(Returns\s*-------\s*)(.*)", re.M | re.S)
    
    reg_groups = body_group.findall(get_doc)

    try:
        new_body += reg_groups[0][0] + reg_groups[0][1]

        parameters_body = reg_groups[0][2].split("\n")
        new_body += format_body(parameters_body) + reg_groups[0][3]
        
        for i in range(4, len(reg_groups[0]) - 1, 2):
            formatted_body = reg_groups[0][i].split("\n")
            formatted_body[0] = f"__{formatted_body[0].strip()}__"
            new_body += format_body(formatted_body) + reg_groups[0][i+1]
        
        last_body = reg_groups[0][len(reg_groups[0]) - 1].split("\n")
        last_body[0] = f"__{last_body[0].strip()}__" 
        new_body += format_body(last_body)
    except IndexError:
        print(get_doc)
        raise IndexError

    return new_body

def format_class_body(clean_doc):
    new_body = ""

    body_group = re.compile(r"(.*)(Attributes\s*----------\s*)(.*)(Methods\s*-------\s*)(.*)", re.M | re.S)
    reg_groups = body_group.findall(clean_doc)

    new_body += reg_groups[0][0] + reg_groups[0][1]

    attributes_body = reg_groups[0][2].split("\n")
    new_body += format_body(attributes_body) + reg_groups[0][3]

    methods_body = reg_groups[0][4].split("\n")
    new_body += format_body(methods_body)

    return new_body

def create_md(module_list):

    character_regex = r"[\\.\>(),_:]"

    f = open(r'TECHSPEC.md', 'w+')
    
    # create table of contents first
    f.write(f"# Table Of Contents\n\n")
    for module_to_print in module_list:
        f.write(f"### From {module_to_print.__name__}\n")
        for i in dir(module_to_print):
            module_attribute = getattr(module_to_print, i)
            if inspect.isclass(module_attribute) and module_attribute.__module__ == module_to_print.__name__:
                ref_string = re.sub(character_regex, "", module_attribute.__name__)
                ref_string = ref_string.replace(" ", "-").lower()
                f.write(f"* [Class {module_attribute.__name__}](#class-{ref_string})\n\n")
                for attribute, function in vars(module_attribute).items():
                    if inspect.isfunction(function):
                        if attribute[0] == "_":
                            attribute = attribute.replace("_", "\_")
                        ref_string = re.sub(character_regex, "", f"{module_attribute.__name__}{attribute}{inspect.signature(function)}")
                        ref_string = ref_string.replace(" ", "-").lower()
                        f.write((f"\t* [{module_attribute.__name__}.{attribute}{inspect.signature(function)}](#{ref_string})\n\n"))
            elif inspect.isfunction(module_attribute) and module_attribute.__module__ == module_to_print.__name__:
                ref_string = re.sub(character_regex, "", f"{module_attribute.__name__}{inspect.signature(module_attribute)}")
                ref_string = ref_string.replace(" ", "-").lower()
                f.write((f"* [{module_attribute.__name__}{inspect.signature(module_attribute)}](#{ref_string})\n\n"))
        f.write(("\n****************************************************\n"))

    # prints out table of contents with anchor links

    # prints out the actual doc strings
    for module_to_print in module_list:
        f.write(f"# From {module_to_print.__name__}\n\n")
        for i in dir(module_to_print):
            module_attribute = getattr(module_to_print, i)
            if inspect.isclass(module_attribute) and module_attribute.__module__ == module_to_print.__name__:
                for attribute, function in vars(module_attribute).items():
                    if attribute == "__doc__":
                        ref_string = re.sub(character_regex, "", module_attribute.__name__)
                        ref_string = ref_string.replace(" ", "-").lower()
                        f.write(f"<a name=\"class-{ref_string}\"></a>\n")
                        f.write(f"## __class {module_attribute.__name__}__\n")
                        f.write((f"{format_class_body(inspect.cleandoc(function))}\n"))
                    elif inspect.isfunction(function):
                        if attribute[0] == "_":
                            attribute = attribute.replace("_", "\_")
                        ref_string = re.sub(character_regex, "", f"{module_attribute.__name__}{attribute}{inspect.signature(function)}")
                        ref_string = ref_string.replace(" ", "-").lower()
                        f.write(f"<a name=\"{ref_string}\"></a>\n")
                        f.write((f"## __{module_attribute.__name__}.{attribute}{inspect.signature(function)}__\n{format_function_body(inspect.getdoc(function))}\n"))
                    f.write(("\n****************************************************\n"))
            elif inspect.isfunction(module_attribute) and module_attribute.__module__ == module_to_print.__name__:
                ref_string = re.sub(character_regex, "", f"{module_attribute.__name__}{inspect.signature(module_attribute)}")
                ref_string = ref_string.replace(" ", "-").lower()
                f.write(f"<a name=\"{ref_string}\"></a>\n")
                f.write((f"## __{module_attribute.__name__}{inspect.signature(module_attribute)}__\n{format_function_body(inspect.getdoc(module_attribute))}"))
                f.write(("\n****************************************************\n"))

    f.close()

import ascii_conversion.views
import base_conv.controllers
import base_conv.models
import base_conv.views
import base_conv.test
import birthday_conversion.views
import prime_gen.views
import main_calc.controllers
import main_calc.models
import main_calc.views
import metric_conv.controllers
import metric_conv.models
import metric_conv.views
import metric_conv.test
import prime_gen.controllers
import prime_gen.models
import prime_gen.views
import prime_gen.test
import temp_conversion.temp_conv_logic
import main

module_list = [
    main,
    ascii_conversion.views,
    base_conv.controllers,
    base_conv.models,
    base_conv.views,
    base_conv.test,
    birthday_conversion.views,
    prime_gen.views,
    main_calc.controllers,
    main_calc.models,
    main_calc.views,
    metric_conv.controllers,
    metric_conv.models,
    metric_conv.views,
    metric_conv.test,
    prime_gen.controllers,
    prime_gen.models,
    prime_gen.views,
    prime_gen.test,
    temp_conversion.temp_conv_logic
]

create_md(module_list)

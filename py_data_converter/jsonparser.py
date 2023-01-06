# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import json
import operator

import sys
from glom import glom


iteritems = operator.methodcaller("items")
unicode = str
basestring = str


# %%----------------------------------------------------------------
def refHandler(content):
    return content.split('/')[-1]


def getKeysofanObj(object, prev_key=None, keys=[]):
    if type(object) != type({}):
        keys.append(prev_key)
        return keys
    new_keys = []
    for k, v in object.items():
        if prev_key != None:
            if k.find('ref') == 1:
                print(k, v)
            new_key = "{}.{}".format(prev_key, k)
        else:
            new_key = k
        new_keys.extend(getKeys(v, new_key, []))
    return new_keys


def get_keys(d, curr_key=[]):

    for k, v in d.items():
        if isinstance(v, dict):
            yield from get_keys(v, curr_key + [k])
        # elif isinstance(v, list):
        #     for i in v:
        #         yield from get_keys(i, curr_key + [k])
        # else:
        #     yield '.'.join(curr_key + [k])


def dict_replace_value(d, old, new):
    x = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = dict_replace_value(v, old, new)
        elif isinstance(v, list):
            v = list_replace_value(v, old, new)
        elif isinstance(v, str):
            v = v.replace(old, new)
        x[k] = v
    return x


def replace_keys(data_dict, key_dict):
    new_dict = {}
    if isinstance(data_dict, list):
        ...
        # dict_value_list = list()
        # for inner_dict in data_dict:
        #     dict_value_list.append(replace_keys(inner_dict, key_dict))
        # return dict_value_list
    else:
        for key in data_dict.keys():
            value = data_dict[key]
            new_key = key_dict.get(key, key)
            if isinstance(value, dict) or isinstance(value, list):
                new_dict[new_key] = replace_keys(value, key_dict)
            else:
                new_dict[new_key] = value
        return new_dict



def walk_json(obj, key_transform):
    assert isinstance(obj, dict)

    def _walk_json(obj, new):

        if isinstance(obj, dict):

            if isinstance(new, dict):
                for key, value in obj.items():

                    new_key = key_transform(key)

                    if isinstance(value, dict):
                        new[new_key] = {}
                        _walk_json(value, new=new[new_key])

                    elif isinstance(value, list):
                        new[new_key] = []
                        for item in value:
                            _walk_json(item, new=new[new_key])

                    else:
                        new[new_key] = value

            elif isinstance(new, list):
                new.append(_walk_json(obj, new={}))

        else:
            new.append(obj)


# %%----------------------------------------------------------------
class OAJsonParser(object):

    def __init__(self, jsonfromsource):

        self.openapi = jsonfromsource['openapi']
        self.title = jsonfromsource['info']['title']
        self.version = jsonfromsource['info']['version']
        self.description = jsonfromsource['info']['description']
        self.models = jsonfromsource['components']['schemas']

    # Return Object as dict 
    def get_dict(self):
        return self.__dict__

    # Return Object as JSON
    def get_json(self):
        return json.loads(json.dumps(self.get_dict()))

    def save_json(self, aOutputFile):
        with open(aOutputFile, 'w') as outfile:
            json.dump(self.get_dict(), outfile)

    def get_models(self):
        all_models = list(self.__dict__['models'].keys())
        return list(self.__dict__['models'].keys())

    def get_model_dict(self, aModelName):

        all_models = self.get_models()

        if aModelName in all_models:
            return (self.__dict__['models'].get(aModelName))['properties']

        return None

    def get_model_json(self, aModelName):

        model = self.get_model_dict(aModelName)

        if not model:
            return None

        return json.loads(json.dumps(model))


# Entry Point
if __name__ == "__main__":

    # Count Arguments
    args = len(sys.argv)

    # Unsupported
    if args < 2 or args > 3:
        print('Usage: python ./this_script.py OpenAPI.json <OUT_FILE> (optional)')
        sys.exit()

    input_filename = sys.argv[1]

    if args == 3:
        ouput_filename = sys.argv[2]

    elif args == 2:
        ouput_filename = input_filename.replace('.json', '-out.json')

    else:
        print('Usage: python ./this_script.py OpenAPI.json <OUT_FILE> (optional)')
        sys.exit()

    source = open(f'{input_filename}')
    source = json.load(source)
    allthekeys = [*get_keys(source)]
    alltheValues = [glom(source, item) for item in allthekeys]
    listofRefitem = [item for item in alltheValues if item.find('#') != -1]

    for item in listofRefitem:
        source = dict_replace_value(source, item, item.split('/')[-1])

    template_ = {'$ref': 'type'}
    replacedRefDict = replace_keys(source, template_)

    # OOP Representation
    openAPI_schema = OAJsonParser(replacedRefDict)

    models = openAPI_schema.get_models()

    print('Models -> ' + str(models))

    for m in models:
        model = openAPI_schema.get_model_dict(m)
        model_json = openAPI_schema.get_model_json(m)

        print('[DICT ' + m + '] -> ' + str(model))
        print('[JSON ' + m + '] -> ' + str(model_json))

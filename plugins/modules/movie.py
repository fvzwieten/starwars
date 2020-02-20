#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: movie

short_description: return the title of a starwars movie

version_added: "2.4"

description:
    - "This module return the box office title for the requested starwars movie number"

options:
    movie:
        description:
            - This is the number of the movie
        required: true
    scheme:
        description:
            - Choose for chronological or released
        required: false
        default: chronological

author:
    - Fred van Zwieten (@fvzwieten)
'''

EXAMPLES = '''
# ask for title of movie 1
- name: give me the title of the first movie (in chronological order)
  starwars:
    movie: 1

# pass in a message and have changed true
- name: give me the title of the first movie made
  starwars:
    movie: 1
    scheme: released

'''

RETURN = '''
title:
    description: The box office title of the movie
    type: str
    returned: always
trilogy:
    description: from which trilogie is this movie part of
    type: str
    returned: always
trilogy_sequence:
    description: which sequence number within the trilogy is this movie
    type: number
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        movie=dict(type='int', required=True),
        scheme=dict(type='str', required=False, default='chronological')
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        title='',
        trilogy='',
        trilogy_sequence=0
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    movies={}
    movies[1] = {"title":"Episode IV – A New Hope","trilogy":"Original","sequence":1}
    movies[2] = {"title":"Episode V – The Empire Strikes Back","trilogy":"Original","sequence":2}
    movies[3] = {"title":"Episode VI – Return of the Jedi","trilogy":"Original","sequence":3}
    movies[4] = {"title":"Episode I – The Phantom Menace","trilogy":"Prequel","sequence":1}
    movies[5] = {"title":"Episode II – Attack of the Clones","trilogy":"Prequel","sequence":2}
    movies[6] = {"title":"Episode III – Revenge of the Sith","trilogy":"Prequel","sequence":3}
    movies[7] = {"title":"Episode VII – The Force Awakens","trilogy":"Sequel","secuence":1}
    movies[8] = {"title":"Episode VIII – The Last Jedi","trilogy":"Sequel","sequence":2}
    movies[9] = {"title":"Episode IX – The Rise of Skywalker","trilogy":"Sequel","sequence":3}

    released=[1,2,3,4,5,6,7,8,9]
    chronological=[4,5,6,1,2,3,7,8,9]

    if module.params['scheme'] == 'released':
        result['title'] = movies[released[module.params['movie']-1]]['title']
        result['trilogy'] = movies[released[module.params['movie']-1]]['trilogy']
        result['trilogy_sequence'] = movies[released[module.params['movie']-1]]['sequence']
    else:
        result['title'] = movies[chronological[module.params['movie']-1]]['title']
        result['trilogy'] = movies[chronological[module.params['movie']-1]]['trilogy']
        result['trilogy_sequence'] = movies[chronological[module.params['movie']-1]]['sequence']

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    result['changed'] = False

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['movie'] < 1 or module.params['movie'] > 9:
        module.fail_json(msg='Movie number must be 1 to 9', **result)
    if module.params['scheme'] != "chronological" and module.params['scheme'] != "released":
        module.fail_json(msg="Scheme must be 'chronological' or 'released'", **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()



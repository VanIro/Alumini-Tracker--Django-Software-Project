hierarchy = ['years','levels','programs','groups']
/////////////////////////////////////////programs
bct_program = {
    'into' : false,
    'tag' : 'groups',
    'value' : 'bct',
    'name' : 'BE Computer(BCT)',
    'members' :[
        {'value':'A'},{'value':'B'},{'value':'C'},{'value':'D'}
    ]
} 
bex_program = {
    'into' : false,
    'tag' : 'groups',
    'value' : 'bex',
    'name' : 'BE Electronics(BEX)',
    'members' :[
        {'value':'A'},{'value':'B'},{'value':'C'},{'value':'D'}
    ]
} 
bei_program = {
    'into' : false,
    'tag' : 'groups',
    'value' : 'bei',
    'name' : 'BEI',
    'members' :[
        {'value':'A'},{'value':'B'},{'value':'C'},{'value':'D'}
    ]
} 
//////////////////////////////////////////////////////////levels
bachelors_level = {
    'into' : true,
    'tag' : 'programs',
    'value':'bachelors',
    'members':[
        bct_program,bex_program,bei_program                                       
    ]
}
//////////////////////////////////////////////////////////years
year_2075 = {
    'into' : true,
    'tag' : 'levels',
    'value': '2075',
    'members': [
               bachelors_level 
            ]
 }
////////////////////////////////////////////////////////
json_obj={
    'into' : true,
    'tag' : 'years',
    'members' : [   
        year_2075
    ]
}
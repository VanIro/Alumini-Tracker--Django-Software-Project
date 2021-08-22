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
msice_program = {
    'into': false,
    'tag': 'groups',
    'value': 'MSICE',
    'name': 'MSc in Information & Communications Engineering (MScICE)',
    'members': [
        { 'value': 'A' }, { 'value': 'B' }, { 'value': 'C' }, { 'value': 'D' }
    ]
    }
mscsk_program = {
    'into': false,
    'tag': 'groups',
    'value': 'MSCSK',
    'name': 'MSc in Computer Systems and Knowledge engineering (MScCKSE)',
    'members': [
        { 'value': 'A' }, { 'value': 'B' }, { 'value': 'C' }, { 'value': 'D' }
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
masters_level = {
    'into': true,
    'tag': 'programs',
    'value': 'masters',
    'members': [
        msice_program, mscsk_program
    ]
}
//////////////////////////////////////////////////////////years
year_2075 = {
    'into' : true,
    'tag' : 'levels',
    'value': '2075',
    'members': [
        bachelors_level, masters_level
            ]
}
year_2074 = {
    'into': true,
    'tag': 'levels',
    'value': '2074',
    'members': [
        bachelors_level, masters_level
    ]
}
////////////////////////////////////////////////////////
json_obj={
    'into' : true,
    'tag' : 'years',
    'members' : [   
        year_2075, year_2075
    ]
}
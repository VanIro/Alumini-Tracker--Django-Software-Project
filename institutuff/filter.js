
//choices = require('./choices.js');


tags=[]
function fill_tag(tag,Members){
    let option=document.createElement('option');
    option.value = -1;
    option.innerHTML = 'none';
    tag.innerHTML='';
    tag.appendChild(option);
    for(let i=0;i<Members.length;i++){
        let option=document.createElement('option');
        option.value  = Members[i].value;
        if(Members[i].name)option.innerHTML = Members[i].name;
        else option.innerHTML = Members[i].value;
        tag.appendChild(option);
    }
}


function createTags_(filters_container,tag_name_list,tags_left_count,tag_id=0,fill=false,JSONobj=null){
    
    //console.log('here I amopopopop');
    let tag = document.createElement('select');
    tag.name = tag_name_list[tag_id];//JSONobj.tag;
    tag.class = tag.name+"_tag";
    tag.id=tag_id;
    tag.onchange=choiceEventTags;
    
    let tag_label_container = document.createElement("div");
    tag_label_container.class = "tag_label_class";
    let label_container = document.createElement("div");
    label_container.class = "tag_label_class";
    label_container.innerHTML=tag.name;
    tag_label_container.appendChild(label_container);

    if(fill){
        fill_tag(tag,JSONobj.members)
    }
    else
        tag_label_container.hidden=true;//();
    tags.push(tag);
    tag_label_container.appendChild(tag);
    filters_container.appendChild(tag_label_container);
    //filters_container.appendChild(tag);
    tags_left_count=Number(tags_left_count);
    if(tags_left_count > 1)
        createTags_(filters_container,tag_name_list,tags_left_count-1,tag_id+1);
}

function createTags(){
    createTags_(document.getElementById('filter_tags'),hierarchy,hierarchy.length,0,true,json_obj);
}

function choiceEventTags(tag_id){
    tag_id=Number(this.id);
    //console.log("whats happening"+tag_id);
    if(tag_id<tags.length-1){
        for(let i=tag_id+2;i<tags.length;i++){
            //delete tags[i] element from dom
            fill_tag(tags[i],[]);
            tags[i].parentElement.hidden=true;
        }
        if(tags[tag_id].selectedIndex==0){//(tags[tag_id].value == -1){
            //delete tags[tag_id+1] element from dom
            fill_tag(tags[tag_id+1],[]);
            tags[tag_id+1].parentElement.hidden=true;
        }
        else{
            //fill_tag() //for tags[tag_id+1]
            Members=json_obj.members;//JSONobj.members;//JSONobj has not been defined yet, hai
            for(let i=0;i<=tag_id;i++){
                Members = Members[tags[i].selectedIndex-1].members;
            }
            fill_tag(tags[tag_id+1],Members);
            tags[tag_id+1].parentElement.hidden=false;
        }
    }
}

function getSelectionsString(){
    str="";
    for(let i=0;i<tags.length;i++){
        if(tags[i].selectedIndex>0)
            str+=tags[i].value+"::";
    }
    document.getElementById("list_recipients").value = str;
    document.getElementById("email_form").submit();
}







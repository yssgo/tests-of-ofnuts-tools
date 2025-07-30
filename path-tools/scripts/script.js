function part_toggle(partSelector){
    let part = document.querySelector(partSelector);
    if (part.style.display=='none')
        part.style.display='block'
    else
        part.style.display='none'
}
// https://stackoverflow.com/a/19844757
function enableStylesheet (node) {
    node.disabled = false;
}

function disableStylesheet (node) {
    node.disabled = true;
}

function brightcss(){
    disableStylesheet(document.querySelector('#dark_style'));
    enableStylesheet(document.querySelector('#default_style'));
}
function darkcss(){
    disableStylesheet(document.querySelector('#default_style'));
    enableStylesheet(document.querySelector('#dark_style'));
}
function createToc(SortType){
    if ( document.querySelector('#TableOfContents') !== null ){
      let obj=document.querySelector('#TableOfContents');
      obj.parentElement.removeChild(obj);
    }    
    let headings=document.querySelectorAll('.plug-in>h2:first-of-type');
	let toc_array=[];
	for(let i=0;i<headings.length;i++){
		map_obj={
			'anchor_id':'',
			'menu_path':'',
			'title': '',
			'translation': ''
		};
		map_obj['anchor_id']='#plugin-'+i;
		map_obj['title'] = headings[i].textContent;
		parent = headings[i].parentElement;
        if(parent && parent.dataset && parent.dataset.menu){
			map_obj['menu_path']=parent.dataset.menu;
        }else{
			map_obj['menu_path']='';
		}
        let rp=/\(([^)]+)\)/;
        if( rp.test(map_obj['title']) ){
           exA=rp.exec(map_obj['title']);
           map_obj['translation']=exA[1];
        }
		toc_array.push(map_obj);
	}
	for(let i=0;i<10;i++){
		toc_array[i]['title'];
	}
    if(SortType=="ByMenu"){
        toc_array.sort(function(a,b){
          let menuA, menuB, textA, textB;
		  menuA=a['menu_path']; menuB=b['menu_path'];
          textA=a['title'];
  	      textB=b['title'];
          if(menuA == '' && menuB == ''){
            return textA.toLowerCase().localeCompare(textB.toLowerCase());
          }      
          else if(menuA == '' && menuB != ''){ 
            return -1;
          }
          else if(menuA != '' && menuB == ''){
            return 1;
          }
          else if(menuA != '' && menuB != ''){            
            if(menuA.toLowerCase().localeCompare(menuB.toLowerCase())){
              return menuA.toLowerCase().localeCompare(menuB.toLowerCase());
            }
            return textA.toLowerCase().localeCompare(textB.toLowerCase());
          }
        });
    }
    else if(SortType=="ByAlphabet"){
        toc_array.sort(function(a,b){
          let textA, textB;
          textA=a['title'];
          textB=b['title'];
          return textA.toLowerCase().localeCompare(textB.toLowerCase());
        });
    }
    else if(SortType=="ByTranslation"){
        toc_array.sort(function(a,b){
			let textA, textB, exA, exB,trA,trB;
			textA=a['title'];
			textB=a['title'];
			trA=a['translation'];
			trB=b['translation'];
			if(trA !="" && trB != ""){
				return trA.toLowerCase().localeCompare(trB.toLowerCase());
			}
			else if(trA == "" && trB == ""){
				return textA.toLowerCase().localeCompare(textB.toLowerCase());            
			}
			else if(trA != "" && trB == ""){
				return -1;
			}
			else if(trA == "" && trB != ""){
				return 1;
			}
        });
    }        
    dv=document.createElement('div');
    dv.setAttribute('id','TableOfContents');
    for(let i=0;i<toc_array.length;i++){
		map_obj=toc_array[i];
		p=document.createElement('p')
        a=document.createElement('a')
        a.setAttribute('href', map_obj['anchor_id']);
        at=document.createTextNode(map_obj['title'])
        a.appendChild(at)
        p.appendChild(a)
        parent=headings[i].parentElement;		
        if(map_obj['menu_path'] != ''){
            menut_t=document.createTextNode(' ('+map_obj['menu_path']+')');
            p.appendChild(menut_t)
        }
        dv.appendChild(p);
    }
    document.getElementById("go-to-home").after(dv)
}
window.onload=function(){
    // brightcss()
    darkcss()
    let headings=document.querySelectorAll('.plug-in>h2:first-of-type');
    headings.forEach(function(item,idx,arr){
        item.setAttribute('id','plugin-'+idx);
    });
    createToc("");
}


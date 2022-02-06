import json
import re

###### How to use ######
## 1, Assign the file path where you want to insert the ToC to the variable
file_path = 'nb_toc.ipynb'
## 2, In that file, create a markdown cell with the following information where you want to insert the ToC
## **ToC**
## 3, `python3 ipynb_toc.py` on terminal`

def ipynb_toc(file_path):
    json_raw = open(file_path, 'r')
    json_dict = json.load(json_raw)
    json_raw.close()

    ## heading_list 見出しテキストのリスト
    ## toc_list 作る用
    ## json書き込む用に書き換えちゃう
    heading_list = []
    heading_num = 0
    for i in json_dict['cells']:
        if i['cell_type'] == 'markdown':
            heading_num_list =[]
            for n,t in enumerate(i['source']):
                if re.match("#+ .+\\n", t):
                    heading_list.append(t)
                    heading_num_list.append(n)
            for k,m in enumerate(heading_num_list):
                mm = m+k
                if m>=1 and re.match('<a id=".+"></a>\\n', i['source'][m-1]):
                    i['source'].pop(m-1)
                    mm-=1
                i['source'][mm:mm] = ['<a id="anchor_'+str(heading_num)+'"></a>\n']
                heading_num+=1

    ## toc_list ToC用のリスト
    ## heading_listから作る
    ## **ToC**って書いてあるマークダウンセルを書き換えちゃう
    toc_list = ['**ToC**\n']
    for n,i in enumerate(heading_list):
        t = re.sub(r'# ', "- [", i) + "]"
        t = re.sub(r'#', "    ", t)
        t = re.sub(r'\n', "", t)
        toc_list.append(t + '(#anchor_' + str(n) +')\n')

    for n,i in enumerate(json_dict['cells']):
        if i['cell_type']=='markdown' and (i['source'][0]=='**ToC**' or i['source'][0]=='**ToC**\\n'):
            i['source'] = toc_list

    output = open(file_path,'w')
    json.dump(json_dict, output)
    output.close()


ipynb_toc(file_path)
# -*- coding: utf-8 -*-

import pgzrun
import os
import parser
import code
import sys
import datetime
import linecache
import traceback
import keyword
import time


limit_row = 20  # 常数，列数限制
limit_len = 60  # 每一行的长度限制
cur_row = 0  # 当前行数
cur_col = 0
col = 20 * [0]  # 每行列数
code_start_pos = [60, 100]
result_start_pos = [63,548]
code_wid = 540 / 60  # 字母宽度
code_hei = 426 / 20  # 字母高度
font_size = 1  # 字体大小
code_content = []  # 列表记录已经写入的内容
run_count = 0
result_count = 0
code_color = [['black']*60 for i in range(20)]
WIDTH = 800
HEIGHT = 800
page_index=1


def set_page_index_two():  # 设置page_index
    global page_index
    page_index = 2

def set_page_index_one():
    global page_index
    page_index = 1

# page 1
# 绘制初始界面
def draw_page1():
    #screen.blit('start_bg', (0, 0))
    button_start.draw()
    button_end.draw()
    heart.draw()
    start_title.draw()
    


# 点击开始/结束按钮
def on_mouse_down_page1(pos):
    if button_start.collidepoint(pos):
        sounds.button.play()
        heart_jump_1_page1()
    elif button_end.collidepoint(pos):
        sounds.button.play()
        heart_letusplay_page1()

# 点击运行/保存/退出按钮
def on_mouse_down_page2(pos):
    if button_music.collidepoint(pos):
        if button_music.image == 'music_unpause':
            music.pause()
            button_music.image = 'music_pause'
        else:
            music.unpause()
            button_music.image = 'music_unpause'
    elif button_run.collidepoint(pos):
        sounds.button.play()
        exec_file()
    elif button_save.collidepoint(pos):
        sounds.button.play()
        save_file()
    elif alien.collidepoint(pos):
        set_alien_hurt()
    elif button_end1.collidepoint(pos):
        sounds.button.play()
        heart.image = 'heart_normal'
        heart.pos = 300,400
        clock.schedule_unique(set_page_index_one, 1.0)
        
        
# 点击开始，心心起跳
def heart_jump_1_page1():
    heart.image = 'heart_happy_1'
    clock.schedule_unique(heart_jump_2_page1, 0.5)

def heart_jump_2_page1():
    global normal_act
    heart.image = 'heart_happy_2'
    animate(heart, pos=(300, -50))
    sounds.act_jump.play()
    clock.schedule_unique(set_page_index_two, 1.0)
    normal_act = 1
    set_alien_normal()


# 点击结束，心心撒娇
def heart_letusplay_page1():
    heart.image = 'letusplay'
    heart.pos = 370, 380
    clock.schedule_unique(heart_letusplay_end_page1, 0.6)

def heart_letusplay_end_page1():
    heart.image = 'heart_normal'
    heart.pos = 300, 400
    letusplay = 'hide'


# page 2

def save_file():
    f = open("my_code.py", "w+")
    global code_content
    for i in range(len(code_content)):
        tmp_str = ''.join(code_content[i]) + '\n'
        f.write(tmp_str)
    f.close()
    # exec_file()

def exec_file():
    global code_content,cur_row,run_count
    f=open('result.txt','w+')
    old_sys_out=sys.stdout
    old_sys_err=sys.stderr
    sys.stdout=f
    sys.stderr=f
    try:
        src = ''
        for i in range(len(code_content)):
            src = src + ''.join(code_content[i]) + '\n'
        exec(src)
    except BaseException as e:
        print(*sys.exc_info())
        ci=code.InteractiveConsole()
        for i in range(len(code_content)):
            ci.push(''.join(code_content[i]))
    f.close()      # result在result.txt里面
    sys.stdout=old_sys_out
    sys.stderr=old_sys_err
    run_count += 1

def draw_result():
    global result_start_pos,code_hei,result_count,run_count
    f = open('result.txt','r')
    lines = f.readlines()
    result_row = 0
    for line in lines:    
        screen.draw.text(str(line), (result_start_pos[0], result_start_pos[1] + code_hei * result_row),
                         color='black', fontname='ubuntumono', fontsize=20)
        result_row += 1
    f.close()

def draw_note_pad():
    screen.blit('code_bg',(55,97))
    screen.blit('result_bg',(55,540))

def draw_str(k):  # 绘制第k行的输入内容
    global code_start_pos, code_wid, code_hei,code_color
    for i in range(len(code_content[k])):
        screen.draw.text(code_content[k][i], (code_start_pos[0] + code_wid * i, code_start_pos[1] + code_hei * k),
                         color=code_color[k][i], fontname='ubuntumono', fontsize=18)


# 绘制桌面精灵
def draw_ailen():  
    alien.draw()


def row_limit_overflow():
    warning("row_limit_overflow!")

def warning(str):
    print(str)

def len_limit_overflow():
    warning("len_limit_overflow!")

def draw_page2():
    #screen.clear()
    button_save.draw()
    button_run.draw()
    button_end1.draw()
    button_music.draw()
    draw_note_pad()
    for i in range(len(code_content)):  # 绘制每一行已输入代码
        draw_str(i)
    # 绘制光标
    screen.draw.text('|', (code_start_pos[0] + code_wid * cur_col, code_start_pos[1] + code_hei * cur_row),
                     color="black", fontname='ubuntumono', fontsize=10, background="white")
    draw_ailen()

# 绘制背景背景
def draw():
    global code_start_pos, code_wid, code_hei,run_count,result_count
    screen.blit('start_bg', (0, 0))
    draw_cloud()
    draw_grass_and_sun()

    if page_index==1:
        draw_page1()
    elif page_index==2:
        draw_page2()
        if run_count > 0:
            draw_result()



def check_time(now_time):
    global count_12pm
    if now_time == '09:00:00':
        sounds.i9am1.play()
        set_alien_9am()
    elif now_time == '12:00:00':
        sounds.i12am1.play()
        set_alien_5pm()
    elif now_time == '17:00:00':
        sounds.i5pm1.play()
        set_alien_5pm()
    elif now_time == '00:00:00':
        sounds.i12pm1.play()
        set_alien_12pm_1()
        count_12pm = 0
        
     # for test
#     elif now_time == '15:40:00':
#         sounds.i12am1.play()
#         set_alien_5pm()
#     elif now_time == '15:41:00':
#         sounds.i5pm1.play()
#         set_alien_5pm()
#     elif now_time == '15:42:00':
#         sounds.i12pm1.play()
#         set_alien_12pm_1()
#         count_12pm = 0
#     elif now_time == '15:43:00':
#         sounds.i9am1.play()
#         set_alien_9am()

old_time=''


def on_key_down(key, mod, unicode):
    global code_content, cur_row, cur_col, col, limit_row, limit_len

    while len(col) < 20:  # 补够col pop的0
        col += [0]

    if chr(key) == '\r':
        if len(code_content) >= limit_row:  # 如果超过20行
            row_limit_overflow()
        else:
            if cur_col < col[cur_row]:
                code_content.insert(cur_row + 1, code_content[cur_row][cur_col:col[cur_row]:1])
                code_content[cur_row] = code_content[cur_row][0:cur_col:1]
                col.insert(cur_row + 1, col[cur_row] - cur_col)
                col[cur_row] = cur_col
            else:
                cur_row += 1
                cur_col = 0
                code_content.insert(cur_row, [])
                col.insert(cur_row, 0)
    elif key == keys.BACKSPACE:  # 删除
        if code_content == [[]]:  # 列表中无元素
            warning("Warning: Nothing to delete")
        else:
            if cur_col == 0:
                if not cur_row == 0:
                    if len(code_content[cur_row]) == 0:  # 列表中当前行无元素，返回上一行
                        code_content.pop(cur_row)
                        col.pop(cur_row)
                        cur_row -= 1
                        cur_col = col[cur_row]
                    else:
                        cur_row -= 1
                        cur_col = col[cur_row]
                        code_content[cur_row] += code_content[cur_row + 1]  # 两行合并
                        col[cur_row] += col[cur_row + 1]
                        col.pop(cur_row + 1)
                        code_content.pop(cur_row + 1)
                else:
                    warning("Warning: Nothing to delete")
            else:  # 列表中当前行有元素
                cur_col -= 1
                col[cur_row] -= 1
                code_content[cur_row].pop(cur_col)
    elif unicode == '':  # 不可识别字符
        pass
    elif key == keys.LEFT:
        if 0 < cur_col:
            cur_col -= 1
        elif cur_col == 0 and (not cur_row == 0):
            cur_row -= 1
            cur_col = col[cur_row]
        else:
            warning("couldn't move left anymore!")
    elif key == keys.RIGHT:
        if cur_col < col[cur_row]:
            cur_col += 1
        elif cur_col == col[cur_row] and (cur_row + 1 < len(code_content)):
            cur_row += 1
            cur_col = 0
        else:
            warning("couldn't move right anymore!")
    elif key == keys.UP:
        if cur_row == 0:
            warning("couldn't move up anymore!")
        else:
            cur_row -= 1
            if col[cur_row] >= cur_col:
                pass
            else:
                cur_col = col[cur_row]
    elif key == keys.DOWN:
        if cur_row + 1 >= len(code_content):
            warning("couldn't move down anymore!")
        else:
            cur_row += 1
            if col[cur_row] >= cur_col:
                pass
            else:
                cur_col = col[cur_row]
    else:   #添加content
        if len(code_content[cur_row]) >= limit_len:
            len_limit_overflow()
        else:
            code_content[cur_row].insert(cur_col, unicode)
            cur_col += 1
            col[cur_row] += 1
        choose_voice()  # 是否触发语音

    print("row:",cur_row)
    print("col:",cur_col)
    print(code_content)
    print(col)
    choose_color()


def choose_color():
    global cur_row, cur_col, code_content,col
    str_model = ['import', 'def', 'if', 'break', 'fuckpm', 'str', 'open', 'print', 'all', 'any', '12pm', '12am', '5pm','9am']
    for i in range(len(code_color[cur_row])):   #只更新当前行的颜色
        code_color[cur_row][i]='black'

    tmp_str=''.join(code_content[cur_row])
    for i in range(len(str_model)): # str_model变色
        index = tmp_str.rfind(str_model[i])
        if not index == -1:
            if index == 0 or (
            not ('a' <= code_content[cur_row][index - 1] <= 'z' or 'A' <= code_content[cur_row][index - 1] <= 'Z')):
                if index + len(str_model[i]) >= col[cur_row]:
                    for l in range(len(str_model[i])):
                        code_color[cur_row][index + l] = 'orange'
                else:
                    if not ('a' <= code_content[cur_row][index + len(str_model[i])] <= 'z' or 'A' <=
                            code_content[cur_row][index + len(str_model[i])] <= 'Z'):
                        for l in range(len(str_model[i])):
                            code_color[cur_row][index + l] = 'orange'

    for i in range(len(keyword.kwlist)):    #自带关键词变色
        index=tmp_str.rfind(keyword.kwlist[i])
        if not index == -1:
            if index==0 or (not ('a'<=code_content[cur_row][index-1]<='z' or 'A'<=code_content[cur_row][index-1]<='Z')):
                if index+len(keyword.kwlist[i])>=col[cur_row]:
                    for l in range(len(keyword.kwlist[i])):
                        code_color[cur_row][index+l]='slateblue'
                else:
                    if not ('a'<=code_content[cur_row][index+len(keyword.kwlist[i])]<='z' or 'A'<=code_content[cur_row][index+len(keyword.kwlist[i])]<='Z'):
                        for l in range(len(keyword.kwlist[i])):
                            code_color[cur_row][index + l] = 'slateblue'


def choose_voice():
    global cur_row, cur_col, code_content, def_count, count_12pm, fupm_count, open_count, print_count, str_count
    str_model = ['import', 'def', 'if', 'break', 'fuckpm', 'str', 'open', 'print', 'all', 'any','12pm','12am','5pm','9am']
    tmp_str = ''.join(code_content[cur_row])
    index = -1
    for i in range(len(str_model)):
        col_index=tmp_str.rfind(str_model[i], max(0, cur_col - 6), cur_col)
        if not col_index == -1:
            if not col_index+len(str_model[i])==cur_col:
                continue
            print(col_index,col_index+len(str_model[i]),cur_col)
            index = i
            print("find", str_model[index], "!")
            if str_model[index] == 'import':
                sounds.import1.play()
                set_alien_import()
            elif str_model[index] == 'def':
                sounds.def1.play()
                set_alien_def_1()
                def_count = 0
            elif str_model[index] == 'if':
                sounds.if1.play()
                set_alien_if()
            elif str_model[index] == 'break':
                sounds.break1.play()
                set_alien_break()
            elif str_model[index] == 'fuckpm':
                sounds.fupm1.play()
                set_alien_fupm_1()
                fupm_count=0
            elif str_model[index] == 'str':
                sounds.str1.play()
                set_alien_str_1()
                str_count = 0
            elif str_model[index] == 'open':
                sounds.open1.play()
                set_alien_open_1()
                open_count = 0
            elif str_model[index] == 'print':
                sounds.print1.play()
                set_alien_print_1()
                print_count = 0
            elif str_model[index] == 'all':
                sounds.all1.play()
                set_alien_all()
            elif str_model[index] == 'any':
                sounds.any1.play()
                set_alien_any()
            elif str_model[index]=='12am':
                sounds.i12am1.play()
                set_alien_5pm()
            elif str_model[index]=='12pm':
                sounds.i12pm1.play()
                set_alien_12pm_1()
                count_12pm = 0
            elif str_model[index]=='9am':
                sounds.i9am1.play()
                set_alien_9am()
            elif str_model[index]=='5pm':
                sounds.i5pm1.play()
                set_alien_5pm()
            break


def on_key_up(key):
    pass


def on_mouse_down(pos):  # button
    if page_index==1:
        on_mouse_down_page1(pos)
    elif page_index==2:
        on_mouse_down_page2(pos)


def on_mouse_up(pos):
    global code_start_pos, code_wid, code_hei, cur_row, cur_col, code_content, col
    x, y = pos
    index_col = 0
    index_row = 0
    # print(x,y)
    if code_start_pos[1] - 20 < y < code_start_pos[1] + 446:
        index_col = (x - code_start_pos[0]) // code_wid
        index_row = (y - code_start_pos[1]) // code_hei

    if 0 <= index_row < len(code_content):
        cur_row = int(index_row)
    elif index_row < 0:
        cur_row = 0
    else:
        cur_row = len(code_content) - 1

    if 0 <= index_col <= col[cur_row]:
        cur_col = int(index_col)
    elif index_col < 0:
        cur_col = 0
    else:
        cur_col = col[cur_row]


# 心心动作

# 心心初始状态  
def set_alien_normal():
    global normal_act
    normal_act = 1
    set_alien_normal_1()    
    
def set_alien_normal_1():
    if normal_act == 1:
        alien.image = 'heart_normal_1'
        clock.schedule_unique(set_alien_normal_2, 0.6)
    
def set_alien_normal_2():
    if normal_act == 1:
        alien.image = 'heart_normal_2'
        clock.schedule_unique(set_alien_normal_3, 0.6)

def set_alien_normal_3():
    if normal_act == 1:
        alien.image = 'heart_normal_3'
        clock.schedule_unique(set_alien_normal_1, 0.6)


# 点击心心
def set_alien_hurt():
    global normal_act
    normal_act = 0
    alien.image = 'heart_dislike'
    sounds.act_click.play()
    clock.schedule_unique(set_alien_normal, 1)


# 心心9am
def set_alien_9am():
    global normal_act
    normal_act = 0
    alien.image = 'heart_9_am'
    clock.schedule_unique(set_alien_normal, 5.5)
   
   
# 心心12pm
def set_alien_12pm_1():
    global normal_act
    normal_act = 0
    alien.image = 'heart_sleep_1'
    clock.schedule_unique(set_alien_12pm_2,1)

def set_alien_12pm_2():
    alien.image = 'heart_sleep_2'
    clock.schedule_unique(set_alien_12pm_3,1)
    
count_12pm = 0
def set_alien_12pm_3():
    global count_12pm
    alien.image = 'heart_sleep_3'
    clock.schedule_unique(set_alien_12pm_4,1)
    count_12pm += 1
    
def set_alien_12pm_4():
    alien.image = 'heart_sleep_4'
    if count_12pm < 3:
        clock.schedule_unique(set_alien_12pm_3,1)
    else:
        clock.schedule_unique(set_alien_normal,1)


# 心心5pm（12am）
def set_alien_5pm():
    global normal_act
    normal_act = 0
    alien.image = 'heart_fly'
    animate(alien, tween = 'accelerate',duration = 3,pos = (800,50) )
    clock.schedule_unique(set_alien_5pm_2,3)
    
def set_alien_5pm_2():
    alien.pos = -10,50
    animate(alien,tween = 'decelerate',duration = 2, pos = (100,50))
    clock.schedule_unique(set_alien_normal,2.2)


# 心心import
def set_alien_import():
    global normal_act
    normal_act = 0
    alien.image = 'heart_kiss'
    clock.schedule_unique(set_alien_normal, 0.8)


# 心心if
def set_alien_if():
    global normal_act
    normal_act = 0
    alien.image = 'heart_shy'
    clock.schedule_unique(set_alien_normal, 4.5)


# 心心break
def set_alien_break():
    global normal_act
    normal_act = 0
    alien.image = 'heart_shy'
    clock.schedule_unique(set_alien_normal, 4.5)


# 心心all
def set_alien_all():
    global normal_act
    normal_act = 0
    alien.image = 'heart_smile'
    clock.schedule_unique(set_alien_normal, 3)


# 心心any
def set_alien_any():
    global normal_act
    normal_act = 0
    alien.image = 'heart_shy'
    clock.schedule_unique(set_alien_normal, 4.7)


#心心def
def_count = 0
def set_alien_def_1():
    global def_count, normal_act
    normal_act = 0
    alien.image='heart_def_1'
    clock.schedule_unique(set_alien_def_2,1)
    def_count += 1

def set_alien_def_2():
    alien.image='heart_def_2'
    if def_count < 2:
        clock.schedule_unique(set_alien_def_1, 0.5)
    else:
        clock.schedule_unique(set_alien_normal, 0.5)


#心心fupm
fupm_count=0
def set_alien_fupm_1():
    global fupm_count, normal_act
    normal_act = 0
    alien.image = 'heart_fupm_1'
    clock.schedule_unique(set_alien_fupm_2, 1)
    fupm_count += 1
    
def set_alien_fupm_2():
    alien.image = 'heart_fupm_2'
    if fupm_count < 2:
        clock.schedule_unique(set_alien_fupm_1, 1)
    else:
        clock.schedule_unique(set_alien_normal, 1)
    

#心心open
open_count = 0
def set_alien_open_1():
    global open_count, normal_act
    normal_act = 0
    alien.image = 'heart_happy_1'
    alien.y-=5
    clock.schedule_unique(set_alien_open_2, 1)
    open_count += 1

def set_alien_open_2():
    alien.image = 'heart_happy_2'
    if open_count <2:
        clock.schedule_unique(set_alien_open_1, 1)
    else:
        clock.schedule_unique(set_alien_normal, 1)
        alien.y+=5


#心心print
print_count = 0
def set_alien_print_1():
    global print_count, normal_act
    normal_act = 0
    alien.image='heart_print_1'
    clock.schedule_unique(set_alien_print_2,1)
    print_count += 1

def set_alien_print_2():
    alien.image='heart_print_2'
    if print_count < 2:
        clock.schedule_unique(set_alien_print_1, 1)
    else:
        clock.schedule_unique(set_alien_normal, 1)


#心心str
str_count = 0
def set_alien_str_1():
    global str_count, normal_act
    normal_act = 0
    alien.image='heart_str_1'
    clock.schedule_unique(set_alien_str_2,0.7)
    str_count += 1

def set_alien_str_2():
    alien.image='heart_str_2'
    if str_count< 2:
        clock.schedule_unique(set_alien_str_1, 0.7)
    else:
        clock.schedule_unique(set_alien_normal, 0.7)



# 画云
def draw_cloud():
    cloud.draw()     
# 画 草&太阳
def draw_grass_and_sun():
    grass.draw()
    sun.draw()

#def draw_bg():
    
    
    
def update():
    # 更新云
    cloud.left += 1
    if cloud.left > WIDTH:
        cloud.right = 0
    # 更新 草&太阳&标题
    if int(time.time())%2 == 0:
        grass.image = 'grass_1'
        sun.image = 'sun_1'
        start_title.image = 'start_title_1'
    else:
        grass.image = 'grass_2'
        sun.image = 'sun_2'
        start_title.image = 'start_title_2'
    # 更新时间
    global old_time
    now_time = datetime.datetime.now().strftime('%H:%M:%S')
    if not old_time == now_time:
        check_time(now_time)
    old_time = now_time

    

# page 1

# 放置标题
start_title = Actor('start_title_1')
start_title.center = 400,300

#放置按钮
button_start = Actor('button_start')
button_start.pos = 300,450
button_end = Actor('button_end')
button_end.pos = 500,450

#放置心心
heart = Actor('heart_normal')
heart.pos = 300, 400


# page 2

# 放置精灵
alien = Actor('heart_normal')
alien.pos = 100, 50

# 放置按钮
button_run = Actor('button_run')
button_run.pos = 700,300
button_save = Actor('button_save')
button_save.pos = 700,400
button_end1 = Actor('button_end_1')
button_end1.pos = 700,500
code_content.append([])

# 放置静音
button_music = Actor('music_unpause')
button_music.pos = 700,580

# page 1&2

# 放置云
cloud = Actor('cloud')
cloud.midright = 0,600

# 放置草
grass = Actor('grass_1')
grass.bottomleft = 0,HEIGHT

# 放置太阳
sun = Actor('sun_1')
sun.topright = WIDTH, 0




# 背景音乐
music.play('bgm')


pgzrun.go()

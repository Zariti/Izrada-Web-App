import socket, time, re

def connect_to_server(ip, port, retry = 10):
    s = socket.socket()
    
    try:
        
        s.connect((ip, port))
    except Exception as e:
        print (e)
        if retry > 0:
            time.sleep(1)
            retry -=1
            connect_to_server(ip, port, retry)       
    
    return s

def get_source(s, ip, page): #ovde je ip od hosta

    CRLF = '\r\n'
    get = 'GET /' + page + ' HTTP/1.1' + CRLF
    get += 'Host: '
    get += ip
    get += CRLF
    get += CRLF

    s.send(get.encode('utf-8'))
    response = s.recv(10000000).decode('latin-1')
    print (response)
    return response

def get_all_links(response):
    list_link = []
    beg = 0
    #cnt = 0
    while True:
        beg_str = response.find('href="', beg)   
        if beg_str == -1: #ako ih nema
            return list_link  
        end_str = response.find('"', beg_str + 6)      
        link = response[beg_str + 6:end_str]
        if link not in list_link:
            #if cnt >= 50:      #dopusta max 50 linkova
                #break
            list_link.append(link)
            #cnt += 1            #broji
        beg = end_str + 1
        


        
def check(page): #lnk
    cnt = 0
    main_list = []
    working_links = []
    response = get_source(s, ip, page)
    if response.find('200 OK', 0):
        working_links = get_all_links(response)
        for elem in working_links:
            if elem not in main_list:
                main_list.append(elem)
    cnt += 1
    return main_list

#ip = 'www.crawler-test.com'
ip = 'www.optimazadar.hr'

#ip = 'books.toscrape.com'
port = 80
s = connect_to_server(ip, port)
page = ''
response = get_source(s, ip, page) #salje se zahtjev, dobija se odgovor
print (get_all_links(response), "THIS\n")  #ispisuje sve linkove
cnt = 0
svi_linkovi = []
svi_linkovi = get_all_links(response) #this
print(svi_linkovi)

main_lst = []

cnt = 0
for lnk in svi_linkovi:
    main_lst += (check(lnk))
    cnt += 1
    if cnt > 10:
        break



#print("THE END?: ",main_lst)

last_one = []

for e in main_lst:
    if e not in last_one and 'html' in e:
        last_one.append(e)

print("LISTA: ", last_one)



#working_links = []

#linkovi_koji_rade_glavna = []



    
















#while cnt < 10:
#   for elem in svi_linkovi:
#        response2 = get_source(s, ip, elem)
#        
#        if response2.find('200 OK', 0):
#            if elem not in linkovi_koji_rade:
#                linkovi_koji_rade.append(elem)
#                linkovi_koji_rade_glavna += linkovi_koji_rade
#
 #           print (get_all_links(response2), "\n")
#            cnt += 1
#
#print("LISTA LINKOVA: ", linkovi_koji_rade_glavna)

        

    #print (get_all_links(response), "\n") #ispisivanje svih linkova iz odgovora
import os.path
import sys
import time
import requests
import argparse
from multiprocessing import Process, Lock, Value

lock = Lock()

hosts_filepath = "C:\\Windows\\System32\\drivers\\etc\\hosts"
host_filepath = "C:\\Windows\\System32\\drivers\\etc\\host"

def get(ip, domain, domains_file, sum,s):


    new_txt = os.path.abspath(domains_file)
    ip = ip.strip()
    domain = domain.strip()
    ipd = ip + " : " + domain
    headers = {
        'host': f'{domain}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Referer': 'https://www.google.com',
        'Connection': 'close'
    }

    for i in ("https://", "http://"):
        try:
            url = i + ip
            # lock.acquire()
            # with open(hosts_filepath, 'w+') as f:
            #     f.write(ipd)
            res = requests.get(url=url, timeout=3, headers=headers, verify=False,
                               allow_redirects=False)  # 忽略ssl问题和禁止302、301跳转)
            res_size = len(res.content)
            print("\r" + i + "\t\t" + ipd + "\t" + str(res_size), end="\n")
            print("\r" + "进度百分比：{:.2f}%".format(s.value/sum * 100) + "\t" + "(T_T)",end='')
            with open(new_txt + "\\host.txt", "a+") as f:
                f.write(i + "\t\t" + ipd)
            lock.acquire()
            s.value += 1
            print("\r" + "进度百分比：{:.2f}%".format(s.value / sum * 100) + "\t" + "(T_T)", end='')
            lock.release()
        except:
            lock.acquire()
            s.value += 1
            print("\r" + "进度百分比：{:.2f}%".format(s.value / sum * 100) + "\t" + "(T_T)", end='')
            lock.release()


def test(domains_file, ips_file):
    with open(domains_file, 'r') as d, open(ips_file, 'r') as ip:
        domains = [doamin for doamin in d.readlines()]
        ips = [i for i in ip.readlines()]
    sum = len(domains) * len(ips)
    sum = sum*2
    print("总计{0}组，程序在3s后开始执行,想要停止的赶紧 CTRL+C".format(sum))
    time.sleep(3)
    start_num = 0
    procs = []

    s = Value('i', 0)
    for domain in domains:
        for ip in ips:
            # get(ip,domain)
            procs.append(Process(target=get, args=(ip, domain, domains_file, sum,s)))
            start_num += 1
            print("\r" + "正在整理组：{:.2f}%。整理完后开始host碰撞".format(start_num / sum * 200), end='')
    print()
    print('_________________________________________')
    print()
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()


def main(domains_file, ips_file):
    test(domains_file, ips_file)
    new_path = os.path.abspath(domains_file)

    print('\r________________________________________',end='\n')
    print()
    print("\r" + "进度百分比：100%" + "\t" + "(^_^)")
    print("结果保存在：" + new_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="host碰撞")
    parser.add_argument("-d", "--Domain", help=("传入要碰撞的域名，需要txt文本"))
    parser.add_argument("-ip", "--IP", help=("传入要碰撞的ip，或txt文本"))
    args = parser.parse_args()

    if args.IP:
        if not args.IP.endswith(".txt"):
            print("IP需要传入txt文本")
            sys.exit()
        if args.Domain:
            if not args.Domain.endswith(".txt"):
                print("域名需要传入txt文本")
                sys.exit()
            domains_file = os.path.abspath(args.Domain)
            ips_file = os.path.abspath(args.IP)
            main(domains_file, ips_file)
        else:
            print("域名和ip都需要，你少了域名")
    else:
        print("域名和ip都需要")

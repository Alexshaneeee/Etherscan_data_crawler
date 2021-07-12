import csv
import datetime
import time
import pymysql


def quantity_process(quantity):
    """处理quantity数据"""
    ans = []
    for data in quantity:
        if data == " ":
            continue
        else:
            ans.append(data)
    # print("quantity_length is: {}".format(len(ans)))
    return ans


def from_to_process(from_to):
    """处理from_to数据"""
    data_from = []
    data_to = []
    for i in range(0, len(from_to), 2):
        data_from.append(from_to[i])
    for i in range(1, len(from_to), 2):
        data_to.append(from_to[i])
    # print("data_from length is: {}".format(len(data_from)))
    # print("data_to length is: {}".format(len(data_to)))
    return data_from, data_to


def method_date_process(method_date):
    """处理method和date的数据"""
    method = []
    absolute_time = []
    relative_time = []
    ts = []
    for i in range(0, len(method_date), 3):
        method.append(method_date[i])
    for i in range(1, len(method_date), 3):
        relative_time.append(method_date[i])
    for i in range(2, len(method_date), 3):
        absolute_time.append(method_date[i])
    for date in absolute_time:
        time_format = "%Y-%m-%d %H:%M:%S"
        ts_struct = time.strptime(date, time_format)
        timestamp = time.mktime(ts_struct)
        ts.append(int(timestamp))
    # print("method length is: {}".format(len(method)))
    # print("absolute_time length is: {}".format(len(absolute_time)))
    # print("relative_time length is: {}".format(len(relative_time)))
    return method, absolute_time, ts


def file_write(txn_hash, method, absolute_time, ts, data_from, data_to, quantity, token):
    """将数据写入csv文件中"""
    data_load = []
    data_head = ["ContractAddress", "TxHash", "UnixTimeStamp", "DateTime", "From", "To", "Quantity", "Method"]
    data_length = len(txn_hash)
    for i in range(data_length):
        tem = [token, txn_hash[i], int(ts[i]), absolute_time[i], data_from[i], data_to[i], quantity[i], method[i]]
        data_load.append(tem)
    to_day = datetime.datetime.now()
    name = token + "_{}_{}_{}_{}_{}_{}.csv".format(to_day.year, to_day.month, to_day.day,
                                                   to_day.hour, to_day.minute, to_day.second)
    with open(name, "w", newline="") as file_name:
        csv_writer = csv.writer(file_name, dialect="excel")
        csv_writer.writerow(data_head)
        """for data in data_load:
            csv_writer.writerow(data)"""  # 一行一行写入csv
        csv_writer.writerows(data_load)
    print("done!\noutput to " + name)


def mysql_write(token, txn_hash, ts, absolute_time, data_from, data_to, quantity, method):
    connect = pymysql.connect(
        host='192.168.201.16',
        port=3306,
        user='root',
        passwd='eversec123',
        database='blockchain'
    )
    cursor = connect.cursor()
    data_length = len(txn_hash)

    for i in range(data_length):
        # insert = "INSERT INTO eth_contract_erc20_tx (ContractAddress, TxHash, UnixTimeStamp, DateTime, From, To, " \
        #          "Quantity, Method) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % (
        #              token, txn_hash[i], ts[i], absolute_time[i], data_from[i], data_to[i], quantity[i], method[i])
        insert = "INSERT INTO eth_contract_erc20_tx VALUES('%s','%s',null,'%s','%s','%s','%s','%s','%s')" % (
                     token, txn_hash[i], ts[i], absolute_time[i], data_from[i], data_to[i], quantity[i], method[i])
        print(insert)
        cursor.execute(insert)
    connect.commit()
    print("updating mysql done!")


class EtherscanPipeline:
    def process_item(self, item, spider):
        # 将爬虫item中各项数据取出
        txn_hash = item["txn_hash"]
        method_date = item["method_date"]
        from_to = item["from_to"]
        quantity = item["quantity"]
        # print("Data length:{}".format(len(txn_hash)))
        method, absolute_time, ts = method_date_process(method_date)
        data_from, data_to = from_to_process(from_to)
        quantity = quantity_process(quantity)
        file_write(txn_hash, method, absolute_time, ts, data_from, data_to, quantity, item["token"])
        mysql_write(item["token"], txn_hash, ts, absolute_time, data_from, data_to, quantity, method)
        return item

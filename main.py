from datetime import datetime
import os  # 用于检查文件是否存在

def 创建记录():
    """获取用户输入，带错误检查；输入0返回None退出"""

    # 金额输入（带异常处理）
    while True:  # 循环直到输入正确
        try:
            amount = float(input("\n金额（0退出）:"))
            break  # 转换成功，跳出循环
        except ValueError:
            print("❌ 请输入数字！")
            # 没写break，所以循环继续，重新问

    # 检查退出信号
    if amount == 0:
        return None

    # 类别输入（字符串不怕错，不用try）
    category = input("类别（餐饮/交通/购物）:")

    return {
        "金额": amount,
        "类别": category
    }


def 更新统计(record, food, transport, shopping):
    """根据记录更新三类统计，返回更新后的三个数值"""
    if record["类别"] == "餐饮":
        food += record["金额"]
    elif record["类别"] == "交通":
        transport += record["金额"]
    elif record["类别"] == "购物":
        shopping += record["金额"]

    return food, transport, shopping  # 返回三个值！


def 显示统计(food, transport, shopping, count):
    """格式化显示统计结果"""

    # 空记录检查（用 count，不是 len(records)）
    if count == 0:
        print("\n今日无消费记录，快去花钱吧～")
        return  # 直接结束，后面的都不执行

    #正常执行
    total = food + transport + shopping

    print("\n========== 今日账单 ==========")
    print(f"总笔数：{count} 笔")
    print(f"总支出：{total:.2f} 元")
    print("---------------------------")
    print(f"餐饮：    {food:.2f} 元")
    print(f"交通：    {transport:.2f} 元")
    print(f"购物：    {shopping:.2f} 元")
    print("============================")

def 加载历史记录():
    """启动时调用，返回 records 列表；如果没有文件，返回空列表"""
    if not os.path.exists('账单.csv'):
        print("没有找到历史记录，开始新记账")
        return []

    records = []
    with open('账单.csv', 'r', encoding='utf-8') as f:
        for line in f.read().splitlines():
            if not line:  # 跳过空行
                continue
            category, amount = line.split(',')  # 直接解包赋值
            records.append({
                "类别": category,
                "金额": float(amount)
            })

    print(f"已加载 {len(records)} 条历史记录")
    return records


def 保存记录(records):
    if len(records) == 0:
        print("没有记录需要保存")
        return

    # 生成日期文件名
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f'账单_{today}.csv'  # 例如：账单_2026-03-30.csv

    lines = [f"{r['类别']},{r['金额']}" for r in records]

    with open(filename, 'w', encoding='utf-8-sig') as f:
        f.write("\n".join(lines))

    print(f"已保存到 {filename}，共 {len(records)} 条记录")


# ========== 主程序 ==========

records = 加载历史记录()
food = transport = shopping = 0

# 恢复历史统计（新增）
for r in records:
    if r["类别"] == "餐饮":
        food += r["金额"]
    elif r["类别"] == "交通":
        transport += r["金额"]
    elif r["类别"] == "购物":
        shopping += r["金额"]

print("简易记账本（输入0结束）")

while True:
    record = 创建记录()
    if record is None:
        break

    records.append(record)
    food, transport, shopping = 更新统计(record, food, transport, shopping)

# 显示和保存
显示统计(food, transport, shopping, len(records))
保存记录(records)  # 新增
print("记账结束，拜拜！")


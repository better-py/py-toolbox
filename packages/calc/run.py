import click


def calc(list_a, list_b: list):
    '''
    Convert input to ints because of accuracy issue with float arithmetic.
    '''
    lista, list_b = sorted(list_a), sorted(list_b)
    la_fmt = [int(x * 100) for x in list_a]
    lb_fmt = [int(x * 100) for x in list_b]

    ret = group(la_fmt, lb_fmt)

    # 反转回去
    ans = {round(k / 100, 2): [round(item / 100, 2) for item in v] for k, v in ret.items()}

    for k, v in ans.items():
        print(f"\t🔑ans item: {k}={v}")

    return ans


def group(l1: list, l2: list):
    def backtrack(i, ans):
        #
        # 结束条件
        #
        if i >= len(l2):
            print(f"🚗🚗🚗stop iter, i={i}, len(l2)={len(l2)}, ans={ans[:]}")
            return ans[:]

        ########################################################################

        j = 0
        # print(f"🐛🐛🐛iter l1={l1}, l2={l2}")
        while j < len(l1):
            if l1[j] >= l2[i]:
                # 递归前操作：
                ans.append(j)
                l1[j] -= l2[i]

                print(f"\t💖bef iter: ♥️l1[{j:4d}]-={l1[j]:4d}, ♦️l2[{i:4d}]={l2[i]:4d}， 🔑ans:{ans}")

                ########################################################################
                # 递归前操作：
                a = backtrack(i + 1, ans)

                ########################################################################

                # 递归后操作：
                l1[j] += l2[i]
                ans.pop()
                print(f"\t🌟aft iter: ♥️l1[{j:4d}]+={l1[j]:4d}, ♦️l2[{i:4d}]={l2[i]:4d}， 🔑ans:{ans}")

                #
                if a:
                    # print(f"\t\t💎ans: {a}")
                    return a
            j += 1
        return []

    ########################################################################

    ret = {x: [] for x in l1}

    if sum(l1) != sum(l2):
        # No Answer
        return ret

    ########################################################################
    # 递归调用：
    ans = backtrack(0, [])
    print(f"⚠️⚠️⚠️️real answer: {ans}")

    ########################################################################

    # 构造：
    for i, x in enumerate(ans):
        ret[l1[x]].append(l2[i])
        print(f"\t✅enumerate: i={i:2d}, x={x}, 💎ret={ret}")

    return ret


@click.command()
def main():
    l1 = [23.17, 3.2, 1.22, 0.32]
    l2 = [7.36, 4.16, 3.20, 1.69, 1.28, 1.28, 0.96, 0.96, 0.90, 0.64, 0.64, 0.64, 0.50, 0.50, 0.32, 0.32, 0.32,
          0.32, 0.32, 0.32, 0.32, 0.32, 0.32, 0.32]

    ret1 = calc(l1, l2)

    l1 = [52.7, 8.96]
    l2 = [21.44, 6.72, 5.44, 5.12, 4.48, 3.20, 2.24, 1.92, 1.92, 1.92, 1.28, 1.28, 1.00, 0.96, 0.50, 0.32,
          0.32, 0.32, 0.32, 0.32, 0.32, 0.32]

    ret2 = calc(l1, l2)

    print(f"🔑ans 1 = {ret1}")
    print(f"🔑ans 2 = {ret2}")


if __name__ == '__main__':
    main()

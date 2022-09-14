# Q1
max_value = 50
def gugudan(input_number) :
    print(str(input_number) + " 단")

    gugu_count = 1
    while True :
        result = input_number * gugu_count
        if gugu_count > 9 or result > 50 :
             break
        else:
            if gugu_count % 2 != 0 :
                print("{0} × {1} = {2}".format(input_number, gugu_count, result))

        gugu_count = gugu_count + 1

number = int(input("몇 단? : "))
gugudan(number)

#Q2 
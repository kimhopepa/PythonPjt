class OuterClass:
    member_value = 3
    def __init__(self, value):
        self.value = value
        print(OuterClass.InnerClass.i_member_value)
    class InnerClass:
        i_member_value = 4
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance

        def display_outer_value(self):
            print("Outer class value:", self.outer_instance.value)
            print("OuterClass member_value", OuterClass.member_value )
            __class__.class_func()

        @classmethod
        def class_func(cls):
            sum = 10 + 5
            print(sum)


# 사용 예시
outer = OuterClass(42)
inner = outer.InnerClass(outer)
inner.display_outer_value()
# from package1 import module1
#
# module1.func1()
# from package import module1
# from package.protoss import zealot
# from package.zerg import ring
# from package.teran import marin
#
# marin.func1()
#
# zealot.func1()
#
# ring.func1()

import package.module1 as m1
import package
# from package import module1 as m1

print(package.g_number)

m1.func1()
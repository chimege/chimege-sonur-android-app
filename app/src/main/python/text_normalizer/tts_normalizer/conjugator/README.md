# Conjugator


## Usage

just change the form_conjugations() function arguments for now :)

```
from conjugate import form_conjugations

out = form_conjugations("хах", "V-past")
print(out)
```

## Mongolian verb conjugations

Mongolian verb conjugations are classified in 6 different classes: Үйлийг цагаар төгсгөх нөхцөл, Үйлийн биеэр төгсгөх нөхцөл, Үйлийн тодотгон холбох нөхцөл, Үйлийн нөхцөлдүүлэн холбох нөхцөл, Үйлийн байдлын нөхцөл, Үйлийн хэвийн нөхцөл. 

This conjugator gets a verb and a desired conjugation class code as input, where the class codes are:

| Conjugation   | Code          |
| ------------- |:-------------:|
| цагаар төгсгөх| V-PAST, V-PRESENT-FUTURE |
| биеэр төгсгөх|V-BIYEER-TUGSGUH |
| тодотгон холбох| V-TODOTGON |
|нөхцөлдүүлэн холбох| V-NUHTSULDUULEN |
| байдлын| V-BAIDLIIN|
| хэвийн| V-HEVIIN   |

and outputs a list of all conjugated words. For example:


```
from conjugate import form_conjugations

out = form_conjugations("үйлдэх", "V-todotgon")
print(out)
```

```
OUTPUT: ['үйлдэшгүй', 'үйлдэхүй', 'үйлдэхүйц', 'үйлдэхүүн', 'үйлдсэн', 'үйлдмээр', 'үйлддэг', 'үйлдүүштэй', 'үйлдээгүй', 'үйлдэгч', 'үйлдэлгүй', 'үйлдэх', 'үйлдэлтэй']
```

list of suffixes(?) in the conjugation classes :)

| Conjugation   | Suffixes          |
| ------------- |:-------------:|
| цагаар төгсгөх| V-PAST: -жээ, -чээ, -в, -лаа4,  V-PRESENT-FUTURE: -нам4, -юу, -юү, -на4, -муй|
| биеэр төгсгөх| -я, -е, -ё, -гтун, -гтүн, -г, -аарай4, -аасай4, -аач4, -үүзэй, -уузай, -сүгэй, -сугай, -түгэй, -тугай|
| тодотгон холбох|-сан4, -гч, -маар4, -үүштэй, -ууштай, -шгүй, -лтай3, -лгүй, -аагүй, -ээгүй, -оогүй, -өөгүй|
|нөхцөлдүүлэн холбох| -ч, -ж, -тал4, -хлаар4, -вал4(бал), -вч, -хул, -хүл, -ваас4, -хүйеэ, -хуйяа, -н, -аад4, -магц4, -саар4, нгаа4, -нгуут, -нгүүт, -хаар4, -руун, -рүүн|
| байдлын|-чих, -зана4, -цгаа4, -схий|
| хэвийн|  -уул, -үүл, -аа4, -лга4, -га4, -ха4, -гд, -лд, -лц|

# File Descriptions

## Modified Wave Function with FDM.py

### 개요
이 파일에서는 1차원 파동 방정식에 약간의 수정을 가하여 시뮬레이션을 진행합니다. 파동방정식은 [FDM](https://en.wikipedia.org/wiki/Finite_difference_method)을 이용하여 수치적으로 풀었습니다.

### 1차원 파동 방정식
가장 기본적인 파동 방정식은 아래와 같습니다.

$$\dfrac{\partial^2 u}{\partial t^2} = c^2\dfrac{\partial^2 u}{\partial x^2}$$

이때 $c$는 파동의 전파 속도이고, $u(x, t)$는 $x$ 위치, $t$ 시점에서 수면의 높이입니다. 여기에 물방을 충돌에 의한 외력을 고려합니다.

$$\dfrac{\partial^2 u}{\partial t^2} = c^2\dfrac{\partial^2 u}{\partial x^2} + \dfrac{F(x, t)}{m}$$

이때, $F(x, t)$는 위치 $x$, 시점 $t$에 작용하는 외력입니다. 파이썬에서는 if 문으로 구현할 수 있습니다. 하지만 이렇게만 설정한다면, 실제 수면파와 다르게 파동이 사라지지 않고 사인파와 비슷한 형태로 무한히 진동할 것입니다. 따라서 감쇠항을 추가합니다.

$$\dfrac{\partial^2 u}{\partial t^2} = c^2\dfrac{\partial^2 u}{\partial x^2} + \dfrac{F(x, t)}{m} - \gamma \dfrac{\partial u}{\partial t}$$

$\gamma$는 비례상수입니다. 여기까지가 Chat GPT가 제안한 미분방정식이었습니다. 그러나 이렇게만 구현했더니, 수면에 물방울을 떨어뜨릴 때마다 수면이 아래로 내려가고, 다시 위로 올라오지를 않았습니다. 따라서 복원력 항이 추가되어야 함을 느꼈습니다.

$$\dfrac{\partial^2 u}{\partial t^2} = c^2\dfrac{\partial^2 u}{\partial x^2} + \dfrac{F(x, t)}{m} - \gamma \dfrac{\partial u}{\partial t} -\dfrac{k}{m}(u-u_0)$$

$k$는 비례상수고, $u_0$는 최초 수면 높이입니다. 이 미분방정식에서 비례 상수들을 조절하면서 가장 적절한 비례 상수를 찾았습니다.

### 선형 공기저항을 고려한 물방울 낙하
물방울 낙하를 제대로 구현하기는 어려운 까닭으로, 물방울을 질점으로 가정하고 선형 공기저항을 고려하여 낙하 시뮬레이션을 진행했습니다. 중력은 $F=mg$이고, 공기저항은 $F=-cv$이므로

$$\dfrac{d^2 y}{dt^2} = g - \dfrac{c}{m}\dfrac{dy}{dt}$$

를 풀면 낙하 시뮬레이션을 구현할 수 있습니다.

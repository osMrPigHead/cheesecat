"""那一刻, 他 (Grant Sanderson) 变成了光"""
from customs.coords import *
from customs.wrappers import *
from manimlib import *

__all__ = [
    "SPEED", "WIDTH_RATE",
    "limited", "light_from_path", "transmit_", "transmit",
    "light_path_", "light_path",
    "series_of_light_path_", "series_of_light_path",
    "transmit_light_path_", "transmit_light_path",
    "light_flash_", "light_flash",
    "series_of_light_flash_", "series_of_light_flash",
    "transmit_light_flash_", "transmit_light_flash",
]

SPEED = 1.7
WIDTH_RATE = 0.1  # 决定光在动画中的“拖尾”长度  time_width = width_rate * speed / length

t2v = tuple[vectorlike, vectorlike]
t2vb = tuple[vectorlike, vectorlike, bool]
t2vbb = tuple[vectorlike, vectorlike, bool, bool]
t2vf = tuple[vectorlike, vectorlike, float]
t2vfb = tuple[vectorlike, vectorlike, float, bool]


@ensure_type(CCVector, 0, "light_source")
@ensure_type(CCEquation, 1, "light", builder=CCEquation.build)
def limited(light_source: vectorlike, light: CCEquation | equation_builder,
            lx: tuple[float, float] = (-1, 1), ly: tuple[float, float] = (-1, 1)) \
        -> CCVector:
    """计算一束范围受限的光的终点"""
    xe, ye = light(x=lx[(z := complex(~light)).real > 0]), light(y=ly[z.imag > 0])
    return xe if abs(light_source - xe) < abs(light_source - ye) else ye


@ensure_type(CCVector, 0, 1, "light_source", "light_dest")
def light_from_path(light_source: vectorlike, light_dest: vectorlike) -> tuple[CCVector, CCAngle]:
    """从光源位置、途经点生成 (light_source, light_angle)"""
    return light_source, ~CCEquation.two_points(light_source, light_dest)


@ensure_type(CCEquation, 0, 1, "light", "surface", builder=CCEquation.build)
def transmit_(light: CCEquation | equation_builder,
              surface: CCEquation | equation_builder, n: float = None, *,
              reverse: bool = False) \
        -> tuple[CCVector, CCEquation, CCEquation] | tuple[CCVector, CCEquation] | None:
    """计算折射、反射
    :return: (incident_point, reflected_light, refracted_light) (as CCEquation)"""
    res = [light & surface]
    if res[0] is None:
        return None
    res += [surface * (res[0], i := surface / light)]
    if n is not None:
        r = acos(cos(i := ~-i if reverse else -i) / n)
        res += [surface * (res[0], r if i > ZERO_ANGLE else -r)]
    return tuple(res)


def transmit(light_source: vectorlike, light_angle:anglelike,
             surface: CCEquation | equation_builder, n: float = None, *,
             reflect: bool = True, reverse: bool = False,
             lx: tuple[float, float] = (-1, 1), ly: tuple[float, float] = (-1, 1)) \
        -> list[tuple[CCVector, CCVector] | tuple[CCVector, CCVector, bool]]:
    """计算折射、反射的动画
    :return: (incident_light, reflected_light, refracted_light) (as CCVector pairs)"""
    transmitted = transmit_((light_source, light_angle), surface, n, reverse=reverse)
    res = [(light_source, transmitted[0]),
           (transmitted[0], limited(transmitted[0], transmitted[1], lx, ly))]
    if reverse:
        for i in range(len(res)):
            res[i] = (res[i][1], res[i][0])
        res[0:2] = res[::-1]
    if reflect:
        res[1] = *res[1], False
    else:
        del res[1]
    if n is not None:
        res += [(transmitted[0], limited(transmitted[0], transmitted[-1], lx, ly))]
    return res


def light_path_(start: vectorlike, end: vectorlike, *,
                dashed: bool = False,
                time_start: float = 0, time_end: float = None,
                run_time: float = DEFAULT_ANIMATION_RUN_TIME) \
        -> tuple[ShowCreation, Line, float]:
    """一条光路 (返回结束/开始时间)"""
    return (ShowCreation(mobject := (DashedLine if dashed else Line)(
        coord(start), coord(end), color=YELLOW, **({"dash_length": 0.2} if dashed else {})),
                        time_span=(time_start, res := time_start + run_time)
                        if time_end is None else (res := time_end - run_time, time_end)),
            mobject, res)


def light_path(start: vectorlike, end: vectorlike, *,
               dashed: bool = False,
               time_start: float = 0, time_end: float = None,
               run_time: float = DEFAULT_ANIMATION_RUN_TIME) \
        -> tuple[ShowCreation, Line]:
    """一条光路 (不返回结束/开始时间)"""
    return light_path_(start, end,
                       dashed=dashed,
                       time_start=time_start, time_end=time_end,
                       run_time=run_time)[0:2]


@iterator2list(-1)
def series_of_light_path_(*lights: t2v | t2vb | t2vbb,
                          dashed: bool = False,
                          time_start: float = 0, time_end: float = None,
                          run_time: float = DEFAULT_ANIMATION_RUN_TIME) \
        -> tuple[list[tuple[ShowCreation, Line]], float]:
    """几条光路 (返回结束/开始时间)"""
    cur_time_start = time_start if time_end is None else time_end
    max_time = time_start if time_end is None else time_end
    flag = False
    for light in lights:
        if len(light) == 2:
            light = *light, True, dashed
        if len(light) == 3:
            light = *light, dashed
        if time_end is not None and not flag:
            light = *light[0:2], True, light[3]
            flag = True
        if time_end is None or light[2]:
            yield (ans := light_path_(light[0], light[1], dashed=light[3],
                                      time_start=cur_time_start,
                                      time_end=None if time_end is None else cur_time_start,
                                      run_time=run_time))[0:2]
            if light[2]:
                cur_time_start = ans[2]
        else:
            yield (ans := light_path_(light[0], light[1], dashed=light[3],
                                      time_start=cur_time_start, run_time=run_time))[0:2]
        max_time = max(max_time, ans[2]) if time_end is None else min(max_time, ans[2])
    yield max_time


def series_of_light_path(*lights: t2v | t2vb | t2vbb,
                         dashed: bool = False,
                         time_start: float = 0, time_end: float = None,
                         run_time: float = DEFAULT_ANIMATION_RUN_TIME) \
        -> list[tuple[ShowCreation, Line]]:
    """几条光路 (不返回结束/开始时间)"""
    return series_of_light_path_(*lights,
                                 dashed=dashed,
                                 time_start=time_start, time_end=time_end,
                                 run_time=run_time)[0]


def transmit_light_path_(light_source: vectorlike, light_angle: anglelike,
                         surface: CCEquation | equation_builder, n: float = None, *,
                         reflect: bool = True, reverse: bool = False,
                         lx: tuple[float, float] = (-1, 1), ly: tuple[float, float] = (-1, 1),
                         dashed: bool = False,
                         reflect_dashed: bool = False, refract_dashed: bool = False,
                         time_start: float = 0, time_end: float = None,
                         run_time: float = DEFAULT_ANIMATION_RUN_TIME)\
        -> tuple[list[tuple[ShowCreation, Line]], float]:
    """折射、反射光路 (返回结束/开始时间)"""
    res = transmit(light_source, light_angle,
                   surface, n,
                   reflect=reflect, reverse=reverse,
                   lx=lx, ly=ly)
    if reflect:
        res[1] = *res[1], reflect_dashed
    if n is None:
        res[-1] = *res[-1], refract_dashed
    return series_of_light_path_(*res, dashed=dashed,
                                 time_start=time_start, time_end=time_end, run_time=run_time)


def transmit_light_path(light_source: vectorlike, light_angle:anglelike,
                        surface: CCEquation | equation_builder, n: float = None, *,
                        reflect: bool = True, reverse: bool = False,
                        lx: tuple[float, float] = (-1, 1), ly: tuple[float, float] = (-1, 1),
                        dashed: bool = False,
                        reflect_dashed: bool = False, refract_dashed: bool = False,
                        time_start: float = 0, time_end: float = None,
                        run_time: float = DEFAULT_ANIMATION_RUN_TIME)\
        -> list[tuple[ShowCreation, Line]]:
    """折射、反射光路 (不返回结束/开始时间)"""
    return transmit_light_path_(light_source, light_angle,
                                surface, n,
                                reflect=reflect, reverse=reverse,
                                lx=lx, ly=ly,
                                dashed=dashed,
                                reflect_dashed=reflect_dashed, refract_dashed=refract_dashed,
                                time_start=time_start, time_end=time_end,
                                run_time=run_time)[0]


def light_flash_(start: vectorlike, end: vectorlike, *,
                 time_start: float = 0, time_end: float = None,
                 speed: float = SPEED, width_rate: float = WIDTH_RATE) \
        -> tuple[ShowPassingFlash, float, float]:
    """一束光闪过 (返回结束/开始时间、路径长度)"""
    return (ShowPassingFlash(Line(coord(start), coord(end), color=YELLOW), rate_func=linear,
                             time_width=min(width_rate * speed / (length := abs(start - end)), 1),
                             time_span=(time_start, res := time_start + length / speed)
                             if time_end is None else (res := time_end - length / speed, time_end)),
            res, length)


def light_flash(start: vectorlike, end: vectorlike, *,
                time_start: float = 0, time_end: float = None,
                speed: float = SPEED, width_rate: float = WIDTH_RATE) \
        -> ShowPassingFlash:
    """一束光闪过 (不返回结束/开始时间、路径长度)"""
    return light_flash_(start, end,
                        time_start=time_start, time_end=time_end,
                        speed=speed, width_rate=width_rate)[0]


@iterator2list(-1)
def series_of_light_flash_(*lights: t2v | t2vb | t2vf | t2vfb,
                           time_start: float = 0, time_end: float = None,
                           speed: float = SPEED, width_rate: float = WIDTH_RATE) \
        -> tuple[list[ShowPassingFlash], float]:
    """几束光闪过 (返回结束/开始时间)"""
    if time_end is not None:
        lights = lights[::-1]
    cur_time_start = time_start if time_end is None else time_end
    max_time = time_start if time_end is None else time_end
    flag = False
    for light in lights:
        if len(light) == 2:
            light = *light, speed, True
        if len(light) == 3:
            if isinstance(light[2], bool):
                light = *light[0:2], speed, light[2]
            if isinstance(light[2], float):
                light = *light, True
        if time_end is not None and not flag:
            light = *light[0:3], True
            flag = True
        if time_end is None or light[3]:
            yield (ans := light_flash_(light[0], light[1], time_start=cur_time_start,
                                       time_end=None if time_end is None else cur_time_start,
                                       speed=light[2], width_rate=width_rate))[0]
            if time_end is not None:
                cur_time_start = ans[1] + width_rate
            elif light[3]:
                cur_time_start = ans[1] - width_rate
        else:
            yield (ans := light_flash_(light[0], light[1], time_start=cur_time_start,
                                       speed=light[2], width_rate=width_rate))[0]
        max_time = max(max_time, ans[1]) if time_end is None else min(max_time, ans[1])
    yield max_time


def series_of_light_flash(*lights: t2v | t2vb | t2vf | t2vfb,
                          time_start: float = 0, time_end: float = None,
                          speed: float = SPEED, width_rate: float = WIDTH_RATE) \
        -> list[ShowPassingFlash]:
    """几束光闪过 (不返回结束/开始时间)"""
    return series_of_light_flash_(*lights,
                                  time_start=time_start, time_end=time_end,
                                  speed=speed, width_rate=width_rate)[0]


def transmit_light_flash_(light_source: vectorlike, light_angle: anglelike,
                          surface: CCEquation | equation_builder, n: float = None, *,
                          reflect: bool = True, reverse: bool = False,
                          lx: tuple[float, float] = (-1, 1), ly: tuple[float, float] = (-1, 1),
                          time_start: float = 0, time_end: float = None,
                          speed: float = SPEED, width_rate: float = WIDTH_RATE) \
        -> tuple[list[ShowPassingFlash], float]:
    """折射、反射动画 (返回结束/开始时间)"""
    res = transmit(light_source, light_angle,
                   surface, n,
                   reflect=reflect, reverse=reverse,
                   lx=lx, ly=ly)
    if n is not None:
        res[-1] = *res[-1], speed / n
    return series_of_light_flash_(*res, time_start=time_start, time_end=time_end,
                                  speed=speed, width_rate=width_rate)


def transmit_light_flash(light_source: vectorlike, light_angle: anglelike,
                         surface: CCEquation | equation_builder, n: float = None, *,
                         reflect: bool = True, reverse: bool = False,
                         lx: tuple[float, float] = (-1, 1), ly: tuple[float, float] = (-1, 1),
                         time_start: float = 0, time_end: float = None,
                         speed: float = SPEED, width_rate: float = WIDTH_RATE) \
        -> list[ShowPassingFlash]:
    """折射、反射动画 (不返回结束/开始时间)"""
    return transmit_light_flash_(light_source, light_angle, surface, n,
                                 reflect=reflect, reverse=reverse, lx=lx, ly=ly,
                                 time_start=time_start, time_end=time_end,
                                 speed=speed, width_rate=width_rate)[0]

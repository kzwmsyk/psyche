
from enum import Enum, auto


class ErrorCode(Enum):
    CANT_FIND_ERR = auto()
    ARG_SYM_ERR = auto()
    ARG_NUM_ERR = auto()
    ARG_LIS_ERR = auto()
    ARG_LEN0_ERR = auto()
    ARG_LEN1_ERR = auto()
    ARG_LEN2_ERR = auto()
    ARG_LEN3_ERR = auto()
    MALFORM_ERR = auto()
    CANT_READ_ERR = auto()
    ILLEGAL_OBJ_ERR = auto()

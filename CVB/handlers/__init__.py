from aiogram import Router
from ..utils import scheduler        # now scheduler is CVB/utils/scheduler.py
from ..utils.permissions import is_admin
from .start_handler import router as start_router
from .help_handler import router as help_router
from .price_handler import router as price_router
from .btcprice import router as btcprice_router
from .ethtrend import router as ethtrend_router
from .globalchart import router as globalchart_router
from .wallet_handler import router as wallet_router
from .tip_handler import router as tips_router
from .raid_handler import router as raid_router
from .admin_handler import router as admin_router
from .gban import router as gban_router
from .auto_clean import router as autoclean_router
from .deposit_handler import router as deposit_router
from .withdraw_handler import router as withdraw_router
from .ai_qa_handler import router as ai_qa_router
from .automated import router as automated_router
from .blacklist import router as blacklist_router
from .captcha_modes import router as captcha_router
from .dev_handler import router as dev_router
from .filters_handler import router as filters_router
from .flood_protection import router as flood_router
from .fun_handler import router as fun_router
from .gkick_handler import router as gkick_router
from .moderation import router as moderation_router
from .modules import router as modules_router
from .notes_filters import router as notes_router
from .security import router as security_router
from .slowmode import router as slowmode_router
from .warnings import router as warnings_router
from .balance_handler import router as balance_router
from .ban_handler import router as ban_router
from .misc import router as misc_router
from .payment_handler import router as payment_router
from .stats import router as stats_router
from .threads import router as threads_router
from .unban_handler import router as unban_router
from .user_utils_handler import router as user_utils_router
from .utilities_handler import router as utilities_router



main_router = Router()
main_router.include_router(start_router)
main_router.include_router(help_router)
main_router.include_router(price_router)
main_router.include_router(btcprice_router)
main_router.include_router(ethtrend_router)
main_router.include_router(globalchart_router)
main_router.include_router(wallet_router)
main_router.include_router(tips_router)
main_router.include_router(raid_router)
main_router.include_router(admin_router)
main_router.include_router(gban_router)
main_router.include_router(autoclean_router)
main_router.include_router(deposit_router)
main_router.include_router(withdraw_router)
main_router.include_router(ai_qa_router)
main_router.include_router(automated_router)
main_router.include_router(blacklist_router)
main_router.include_router(captcha_router)
main_router.include_router(dev_router)
main_router.include_router(filters_router)
main_router.include_router(flood_router)
main_router.include_router(fun_router)
main_router.include_router(gkick_router)
main_router.include_router(moderation_router)
main_router.include_router(modules_router)
main_router.include_router(notes_router)
main_router.include_router(security_router)
main_router.include_router(slowmode_router)
main_router.include_router(warnings_router)
main_router.include_router(balance_router)
main_router.include_router(ban_router)
main_router.include_router(misc_router)
main_router.include_router(payment_router)
main_router.include_router(stats_router)
main_router.include_router(threads_router)
main_router.include_router(unban_router)
main_router.include_router(user_utils_router)
main_router.include_router(utilities_router)

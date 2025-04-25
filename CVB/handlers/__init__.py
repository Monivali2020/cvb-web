#CVB/handlers/__init__.py

from aiogram import Router

# Import your routers
from .start_handler       import router as start_router
from .help_handler        import router as help_router
from .price_handler       import router as price_router
from .btcprice            import router as btcprice_router
from .ethtrend            import router as ethtrend_router
from .globalchart         import router as globalchart_router
from .wallet_handler      import router as wallet_router
from .tips_handler        import router as tips_router
from .raid_handler        import router as raid_router
from .admin_handler       import router as admin_router
from .gban                import router as gban_router
from .auto_clean          import router as autoclean_router
from .deposit_handler     import router as deposit_router
from .withdraw_handler    import router as withdraw_router
from .ai_qa_handler       import router as ai_qa_router
from .automated           import router as automated_router
from .blacklist           import router as blacklist_router
from .captcha_modes       import router as captcha_router
from .dev_handler         import router as dev_router
from .filters_handler     import router as filters_router
from .flood_protection    import router as flood_router
from .fun_handler         import router as fun_router
from .kick                import router as kick_router
from .gkick_handler       import router as gkick_router
from .moderation          import router as moderation_router
from .modules             import router as modules_router
from .notes_filters       import router as notes_router
from .security            import router as security_router
from .slowmode            import router as slowmode_router
from .warnings            import router as warnings_router
from .balance_handler     import router as balance_router
from .ban_handler         import router as ban_router
from .misc                import router as misc_router
from .payment_handler     import router as payment_router
from .stats               import router as stats_router
from .threads             import router as threads_router
from .unban_handler       import router as unban_router
from .user_utils_handler  import router as user_utils_router
from .utilities_handler   import router as utilities_router

# Create and wire up the main router
main_router = Router()
for r in (
    start_router, help_router, price_router, btcprice_router, ethtrend_router, globalchart_router,
    wallet_router, tips_router, raid_router, admin_router, gban_router, autoclean_router,
    deposit_router, withdraw_router, ai_qa_router, automated_router, blacklist_router,
    captcha_router, dev_router, filters_router, flood_router, fun_router, kick_router, gkick_router,
    moderation_router, modules_router, notes_router, security_router, slowmode_router,
    warnings_router, balance_router, ban_router, misc_router, payment_router, stats_router,
    threads_router, unban_router, user_utils_router, utilities_router,
):
    main_router.include_router(r)
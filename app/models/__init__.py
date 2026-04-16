from app.database import Base  # noqa: F401 — importar Base antes de los modelos
from app.models.institution import Institution  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.credit_type import CreditType  # noqa: F401
from app.models.indirect_charge import IndirectCharge  # noqa: F401
from app.models.amortization import AmortizationSchedule  # noqa: F401
from app.models.investment_type import InvestmentType  # noqa: F401
from app.models.investment import InvestmentSimulation, InvestmentApplication, KYCDocument  # noqa: F401

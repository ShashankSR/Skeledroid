
list1 = ["activity", "SupportActivity", "SignUpMobileVerificationActivity", "AccountService", "HomeActivity", "SignInActivity", "CountrySelectionActivity", "CitySelectionActivity"]
list1 = list(set(list1))
list2 = ["activity", "SignUpActivity", "SignOutActivity", "CreatePasswordActivity", "SupportActivity", "CountrySelectionActivity", "HomeActivity", "HomeActivity", "MobileVerificationActivity", "TwoFactorAuthMobileVerificationActivity", "SignInMobileVerificationActivity", "ForgotPasswordActivity", "AccountService", "AccountService", "AccountService"]
list2 = list(set(list2))
print list2 + list(set(list1) - set(list2))
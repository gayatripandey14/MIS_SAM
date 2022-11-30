from users.models import WalletPassbook

def walletlog(current_value,previous_value,request,instance):
    
    if current_value != previous_value:

        amount = current_value - previous_value
        
        if current_value > previous_value:
            transanction_type = "Credit"
        else:
            transanction_type = "Debit"
        
        

        # reciever Logs
        WalletPassbook.objects.using("users_db").create(
                user=instance.user,
                transanction_type=transanction_type,
                amount = amount,
                recieved_from = request.user,
                wallet=instance,
                available_balance=current_value ,
                deduction_rate = instance.service.deduction_rate
            )
        #  sender Logs 
        WalletPassbook.objects.using("users_db").create(
                user= request.user,
                transanction_type=transanction_type,
                amount = amount,
                sent_to = instance.user,
                deduction_rate = instance.service.deduction_rate
            )
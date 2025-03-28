from simiir.user.serp_impressions.base import BaseSERPImpression

class SimpleSERPImpression(BaseSERPImpression):
    """
    A simple approach to SERP impression judging.
    The de facto approach used in prior simulations; assume it's worth examining. Always return True.
    Also includes code to judge the patch type, a different thing from determining if the patch should be entered or not.
    """
    def __init__(self, user_context, qrel_file, host=None, port=None):
        super(SimpleSERPImpression, self).__init__(user_context=user_context,
                                                 qrel_file=qrel_file,
                                                 host=host,
                                                 port=port)
    
    
    def is_serp_attractive(self):
        """
        Determines whether the SERP is attractive.
        As this is the SimpleSERPImpression, the SERP is always considered attractive.
        This will mean at least one snippet will be examined by the simulated user.
        
        For more complex SERP examination strategies, override this method.
        """
        patch_judgements = self._get_patch_judgements()  # We don't have a means of working out judgements for
                                                          # determining patch type, so fall back to TREC judgements.
        patch_type = self._calculate_patch_type(patch_judgements)
        self._set_query_patch_type(patch_type)
        
        return True
#include "config.h"

#if USE_AZURE_BLOB_STORAGE

#include <gtest/gtest.h>

#include <IO/AzureBlobStorage/isRetryableAzureException.h>

TEST(IsRetryableAzureException, RequestTimeoutIsRetryable)
{
    Azure::Core::RequestFailedException exception("request timeout");
    exception.StatusCode = Azure::Core::Http::HttpStatusCode::RequestTimeout;

    EXPECT_TRUE(DB::isRetryableAzureException(exception));
}

#endif

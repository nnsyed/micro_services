package com.demo.cacheservice;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/cache")
public class CacheController {

    @Autowired
    private StringRedisTemplate redisTemplate;

    // Fixed: Capital 'G' for GetMapping
    @GetMapping
    public Map<String, Object> readAllCache() {
        Set<String> keys = redisTemplate.keys("*");
        Map<String, String> cacheDump = new HashMap<>();
        
        if (keys != null) {
            for (String key : keys) {
                cacheDump.put(key, redisTemplate.opsForValue().get(key));
            }
        }
        
        Map<String, Object> response = new HashMap<>();
        response.put("data", cacheDump);
        return response;
    }

    // Fixed: Capital 'P' for PostMapping
    @PostMapping
    public Map<String, String> setCache(@RequestBody Map<String, String> payload) {
        redisTemplate.opsForValue().set(payload.get("key"), payload.get("value"));
        return Collections.singletonMap("status", "success");
    }

    // Fixed: Capital 'D' for DeleteMapping
    @DeleteMapping("/{key}")
    public Map<String, String> deleteCache(@PathVariable String key) {
        redisTemplate.delete(key);
        return Collections.singletonMap("status", "evicted");
    }

    /**
     * GET /cache/{key}
     * Fetches a value from the Redis cache instance directly by key string.
     */
    @GetMapping("/{key}")
    public ResponseEntity<?> getCacheValue(@PathVariable("key") String key) {
        // Look up the key in the Redis memory engine
        String value = redisTemplate.opsForValue().get(key);
        
        // If the key doesn't exist, return a clean 404 block
        if (value == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(Map.of(
                    "status", 404,
                    "error", "Not Found",
                    "message", "Key '" + key + "' was not found in the Redis cache cluster."
                ));
        }
        
        // Return the key-value payload successfully
        return ResponseEntity.ok(Map.of(
            "key", key,
            "value", value
        ));
    }
}